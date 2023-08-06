import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import os

# 设定画图参数
sns.set(style="white", palette="muted", color_codes=True)
plt.rcParams["font.sans-serif"] = ["SimHei"] # 中文字体显示
plt.rcParams["axes.unicode_minus"] = False # 负号正常显示
mpl.rcParams["figure.autolayout"] = True # 自动排版

params = {
    "font.size": 12, # 全局字号
    "figure.subplot.wspace":0.2, # 图-子图-宽度百分比
    "figure.subplot.hspace":0.4, # 图-子图-高度百分比
    "axes.spines.right":False,  # 坐标系-右侧线
    "axes.spines.top":False,   # 坐标系-上侧线
    "xtick.direction":'in',   # 刻度-方向
    "ytick.direction":'in'  # 刻度-方向
}

mpl.rcParams.update(params)

# ---------------------------------------------------------------------------------------------------------------------

class colafactor:
    
    def __init__(self, factor, rets, sector_data=None, asset_type="industry", factor_name="unnamed", quantile=5, freq="M", start_date=None, end_date=None):
        """
        :param factor: 资产的因子数据，索引为日期和资产，日期统一为"%Y-%m-%d"形式
        :param rets: 资产的收益率数据，索引为日期和资产
        :param sector_data: 资产所属板块，无索引，列为日期、资产和板块（股票）或资产和板块（行业）；如果是None，则不考虑板块内轮动
        :param asset_type: 资产类型，"industry"或"stock"，分别代表行业轮动和选股策略
        :param factor_name: 因子名称，用于导出文件和图片时命名，默认为“unnamed”
        :param quantile: 分组数，默认为5
        :param freq: 调仓频率，默认为“M”，即每月
        :param start_date: 回测起始日期
        :param end_date: 回测结束日期
        """
        
        # 因子、收益率、分组、调仓频率
        self.asset_type = asset_type # 资产类型
        self.factor, self.rets, self.sector_data = self.check_input_data_format(factor, rets, sector_data, start_date, end_date)
        self.quantile = quantile # 分组个数
        self.quantile_labels = ["G"+str(i) for i in range(1, quantile+1)] # ["G1", "G2", ..., "G5"]
        self.freq = freq # 调仓频率
        
        # 清洗后的因子数据，之后的计算都是基于data或data_ex
        self.factor_data, self.factor_data_ex = self.get_clean_factor_and_forward_return() 
        
    def check_input_data_format(self, factor, rets, sector_data, start_date=None, end_date=None):
        """检查和规范因子、收益率、板块数据的格式"""
        # 如果 factor 或 rets 是 Series, 转换成 DataFrame
        if isinstance(factor, pd.Series):
            factor = pd.DataFrame(factor)
        if isinstance(rets, pd.Series):
            rets = pd.DataFrame(rets)
            
        # 修改 factor 和 rets 的列名和索引名
        factor.columns = ["Factor"]
        factor.index.names = ["Date", "Asset"]
        rets.columns = ["Return"]
        rets.index.names = ["Date", "Asset"]
        
        # 限定日期：如果没有指定日期，则默认为因子数据的起止日期
        if start_date is None:
            self.start_date = factor.index.get_level_values(0)[0].strftime("%Y-%m-%d")
        else:
            self.start_date = start_date
        if end_date is None:
            self.end_date = factor.index.get_level_values(0)[-1].strftime("%Y-%m-%d")
        else:
            self.end_date = end_date
        
        factor = factor.loc[self.start_date:self.end_date]
        rets = rets.loc[self.start_date:self.end_date]
        
        # 板块数据的格式检查
        ## 如果是行业轮动，行业和板块的匹配不随时间变化，所以合并时只需要on="Asset"
        ## 如果是选股，股票和板块的匹配随时间变化，所以合并时需要on=["Date", "Asset"]
        if sector_data is not None:
            if isinstance(sector_data, pd.Series):
                sector_data = sector_data.reset_index()
            if self.asset_type == "industry":
                sector_data.columns = ["Asset", "Sector"]
            elif self.asset_type == "stock":
                sector_data.columns = ["Date", "Asset", "Sector"]

        return factor, rets, sector_data
        
    def merge_asset_and_sector(self, data):
        """合并资产和所属板块"""
        # 如果data是Series，则转换为DataFrame
        if isinstance(data, pd.Series):
            data = data.to_frame()
        # 如果data没有Asset列，则重置索引，因为可能索引是日期+资产
        if "Asset" not in data.columns:
            data.reset_index(inplace=True)
        # 如果重置后还是没有Asset列，则报错
        if "Asset" not in data.columns:
            raise ValueError("data中没有Asset列，瓜皮")
        # 合并data和sector_data
        if self.asset_type == "industry":
            data = data.merge(self.sector_data, on="Asset", how="left")
        elif self.asset_type == "stock":
            data = data.merge(self.sector_data, on=["Date", "Asset"], how="left")
        return data
    
    def get_clean_factor(self, factor):
        """
        clean_factor是清洗过的因子数据，索引是日期+资产。
        这里进行两个处理，一是只取调仓日的数据并滞后一期，二是删除资产个数少于quantile的日期
        """
        # 以月度调仓为例
        # 每个月月底显示的因子值都是上一个月月底对应的值，因为分组是基于上个月月底的因子来分的
        # 先unstack把索引变成日期，然后只取调仓日的因子数据，接着shift一个月，再stack回去
        refer_data = self.factor.unstack()["Factor"]
        rebalancing_index = refer_data.groupby(refer_data.index.to_period(self.freq)).apply(lambda x: x.index.max())
        clean_factor = factor.unstack()["Factor"].loc[rebalancing_index].shift().stack()
        
        # 删除资产个数少于quantile的日期，因为这些日期无法分组
        tmp = clean_factor.groupby("Date").count() # 统计每天的资产个数
        del_idx = tmp[tmp<self.quantile].index # 取出资产个数少于quantile的日期
        clean_factor = clean_factor[~clean_factor.index.get_level_values(0).isin(del_idx)]
        
        return clean_factor
    
    def get_clean_rets(self, rets):
        """
        clean_rets是清洗过的收益率数据，索引是日期，列为资产
        """
        # 计算两个调仓日之间的收益率之和
        refer_data = self.rets.unstack()["Return"]
        rebalancing_index = refer_data.groupby(refer_data.index.to_period(self.freq)).apply(lambda x: x.index.max())
        clean_rets = refer_data.groupby(refer_data.index.to_period(self.freq)).apply(lambda x: x.sum()).replace(0, np.nan)
        clean_rets.index = rebalancing_index.values
        clean_rets.index.name = "Date"
        return clean_rets
    
    def get_excess_rets(self, clean_rets):
        """
        excess_rets是超额收益率，索引为日期，列为资产。基准为资产等权。
        """
        excess_rets = clean_rets.sub(clean_rets.mean(axis=1), axis=0) # 月度超额收益率
        return excess_rets
    
    def get_forward_rets(self, clean_factor, clean_rets, factor_quantile):
        """
        计算未来十二个月的收益率
        """
        data = pd.DataFrame({"Factor": clean_factor, "Factor_quantile": factor_quantile, "Forward_1": clean_rets.stack()})
        for i in range(2, 13):
            data[f"Forward_{i}"] = clean_rets.shift(-1*(i-1)).stack()
        return data

    def get_factor_quantile(self, clean_factor):
        """
        根据因子得分进行分组
        """
        ## 如果某一期无法分组，就返回None
        def my_cut(x):
            try:
                return pd.qcut(x, self.quantile, labels=["G"+str(i) for i in range(1, self.quantile+1)])
            except:
                return None
        factor_quantile = clean_factor.groupby("Date", group_keys=False).apply(lambda x: my_cut(x))
        return factor_quantile
		
        
    def get_clean_factor_and_forward_return(self):
        """
        获取清洗后的因子数据和收益率数据
        
        return
        ------
        data: 索引为“日期+资产”，列为因子、分组以及未来十个月的收益率
        data_ex: 索引为“日期+资产”，列为因子、分组以及未来十个月的超额收益率
        """
        
        # 获取月度因子数据和分组数据
        clean_factor = self.get_clean_factor(self.factor)
        factor_quantile = self.get_factor_quantile(clean_factor)
        
        # 获取月度收益率数据
        clean_rets = self.get_clean_rets(self.rets)
        excess_rets = self.get_excess_rets(clean_rets)
        
        # 合并因子数据和收益率数据
        factor_data = self.get_forward_rets(clean_factor, clean_rets, factor_quantile)
        factor_data_ex = self.get_forward_rets(clean_factor, excess_rets, factor_quantile)
            
        # 把超额收益率除以该期所在组的资产数量，方便后续计算
        indnum_by_group = factor_data_ex.groupby(["Date", "Factor_quantile"]).Factor.count() # 每期各组的行业数量
        indnum_by_group.name = "Indnum" # 重命名series
        tmp = factor_data_ex.join(indnum_by_group, on=["Date", "Factor_quantile"], how="left") # 合并原始数据和行业数量
        factor_data_ex = tmp[[f"Forward_{i}" for i in range(1, 13)]+["Indnum"]].apply(lambda s: s/s.Indnum, axis=1) # 将超额收益率除以行业数量
        factor_data_ex = factor_data_ex[[f"Forward_{i}" for i in range(1, 13)]].join(tmp[["Factor", "Factor_quantile"]], on=['Date', 'Asset'], how='left')

        # 合并板块数据
        if self.sector_data is not None:
            factor_data = self.merge_asset_and_sector(factor_data).set_index(["Date", "Asset"])
            factor_data_ex = self.merge_asset_and_sector(factor_data_ex).set_index(["Date", "Asset"])
            
        return factor_data, factor_data_ex
    
    # ------------------- IC分析 --------------------------

    def factor_information_coefficient(self, by_sector=False):
        """计算因子的IC序列, spearman 相关系数（序相关系数）, 得到的是 Rank IC
        
        通过ic_all，可以计算累计IC、IC统计量、IC衰减
        
        ic_cum = ic.cumsum() # 累计IC
        
        ic = ic_all.Forward_1 # IC
        ic_mean = ic.mean() # IC 均值
        icir = ic.mean() / ic.std() # ICIR
        ic_t = ic.mean() / ic.std() * np.sqrt(ic.shape[0]-1) # IC_t
        ic_winrate = (ic>0).sum() / ic.shape[0] # IC 序列的胜率：IC 向上的占比
        
        ic_decay = ic_all.mean() # IC衰减
        """
        
        grouper = ["Date"]
        if by_sector:
            grouper.append("Sector")
            
        ic_all = self.factor_data.groupby(grouper).apply(lambda x: x.corr(method="spearman")["Factor"]).drop(columns=["Factor"])
        return ic_all

    def factor_IC_stats(self, by_sector=False):
        """
        计算IC的统计量
        
        IC的绝对值大于0.03时，因子的择股(行业)能力较强, IR大于0.5时因子稳定获取超额收益能力较强
        """
        # 先计算全样本的IC
        ic_all = self.factor_information_coefficient(by_sector=False)
        ic = ic_all.Forward_1 # IC 序列
        ic_mean = ic.mean() # IC 均值
        icir = ic.mean() / ic.std() # ICIR
        ic_t = ic.mean() / ic.std() * np.sqrt(ic.shape[0]-1) # IC_t：用于检查 IC 值序列均值是否显著不为 0
        ic_winrate = (ic>0).sum() / ic.shape[0] # IC 序列的胜率：IC 向上的占比
        
        result = pd.Series({'IC 均值': ic_mean, "IC IR": icir, 'IC T值': ic_t, 'IC 胜率': ic_winrate}, name="全样本")
        
        if by_sector: # 分板块计算IC
            ic_all = self.factor_information_coefficient(by_sector=by_sector)
            ic = ic_all.Forward_1 # IC序列
            ic_mean = ic.groupby("Sector").mean() # 各板块的IC均值
            icir = ic.groupby("Sector").mean() / ic.groupby("Sector").std() # ICIR
            ic_t = icir * ic.groupby("Sector").apply(lambda x: np.sqrt(x.shape[0]-1)) # IC_t
            ic_winrate = ic.groupby("Sector").apply(lambda x: (x>0).sum() / x.shape[0]) # IC序列的胜率

            results = pd.DataFrame({'IC 均值': ic_mean, "IC IR": icir, 'IC T值': ic_t, 'IC 胜率': ic_winrate}).T
            results["全样本"] = result
        else: # 不分板块的话，就直接返回全样本的结果
            results = result
            
        return results

    def factor_IC_cum(self, by_sector=False):
        """
        计算累计IC
        """
        if by_sector:
            # 各板块的累计IC
            ic_all = self.factor_information_coefficient(by_sector)
            ic = ic_all.Forward_1 # IC序列
            ic_cum = ic.groupby("Sector").cumsum().unstack() # 各板块的累计IC
            
            # 全样本的累计IC
            ic_all = self.factor_information_coefficient(by_sector=False)
            ic = ic_all.Forward_1 # IC序列
            ic_cum["全样本"] = ic.cumsum() # 全样本的累计IC
        else:
            # 全样本的累计IC
            ic_all = self.factor_information_coefficient(by_sector)
            ic = ic_all.Forward_1 # IC
            ic_cum = ic.cumsum() # 累计IC
            ic_cum.name = "全样本"
        return ic_cum

    def factor_IC_decay(self, by_sector=False):
        """
        计算因子IC的衰减
        """
        ic_all = self.factor_information_coefficient(by_sector)
        ic_decay = ic_all.mean() # IC衰减
        ic_decay.index = [f"M{i}" for i in range(1, 13)] # 重命名索引
        return ic_decay


    # ----------------------- 收益率分析 -------------------------

    def excess_returns_by_group(self, by_sector=False):
        """每期每个组别的超额收益率"""
        if by_sector:
            grouper = ["Sector", "Date", "Factor_quantile"]
        else:
            grouper = ["Date", "Factor_quantile"]
        excess_rets = self.factor_data_ex.groupby(grouper)["Forward_1"].sum().unstack()
        return excess_rets

    def excess_nav_by_group(self, by_sector=False):
        """每期每个组别的超额净值"""
        excess_rets = self.excess_returns_by_group(by_sector)
        
        if by_sector:
            excess_nav = excess_rets.groupby("Sector").cumsum()
        else:
            excess_nav = excess_rets.cumsum()
        excess_nav = excess_nav.join(pd.Series(excess_nav.iloc[:,-1] - excess_nav.iloc[:,0], name=f"{self.quantile_labels[-1]}-{self.quantile_labels[0]}"))
        return excess_nav

    def stats_alpha_by_group(self, by_sector=False):
        """
        计算因子的alpha。G1-G5组合的收益率减去基准(行业等权组合)的收益率
        """
        excess_rets = self.excess_returns_by_group(by_sector)
        
        if by_sector:
            # 整体表现
            alpha = excess_rets.groupby("Sector").sum()
            
            # 分年分组表现
            grouper = ["Sector", excess_rets.index.get_level_values(1).year]
            alpha_by_year = excess_rets.groupby(grouper).sum() 
            
        else:
            # 整体表现
            alpha = excess_rets.sum() 
            
            # 分年分组表现
            grouper = [excess_rets.index.year]
            alpha_by_year = excess_rets.groupby(grouper).sum() 
        
        return alpha, alpha_by_year
    
    def stats_alpha_by_group_and_month(self, by_sector=False):
        """
        计算因子分组分月的alpha
        """
        excess_rets = self.excess_returns_by_group(by_sector)
        
        if by_sector:
            grouper = ["Sector", excess_rets.index.get_level_values(1).year, excess_rets.index.get_level_values(1).month]
            alpha_by_year_and_month = excess_rets.groupby(grouper).sum()
            alpha_by_year_and_month.index.names = ["Sector", "Year", "Month"]
            alpha_by_month = alpha_by_year_and_month.groupby(["Sector", "Month"]).mean()
            
        else:
            grouper = [excess_rets.index.year, excess_rets.index.month]
            alpha_by_year_and_month = excess_rets.groupby(grouper).sum()
            alpha_by_year_and_month.index.names = ["Year", "Month"]
            alpha_by_month = alpha_by_year_and_month.groupby(["Month"]).mean()
            
        return alpha_by_month
        
    def stats_winrate_by_group(self):
        """
        计算因子的胜率，胜率是组合表现超过基准的月份占比。
        """
        excess_rets = self.factor_data_ex.groupby(["Date", "Factor_quantile"])["Forward_1"].sum().unstack()
        
        # 整体表现
        winrate = (excess_rets>0).sum() / excess_rets.shape[0]
        
        # 分年分组表现
        grouper = [excess_rets.index.year]
        winrate_by_year = (excess_rets > 0).groupby(grouper).mean()
        
        return winrate, winrate_by_year

    def stats_hitrate_by_group(self):
        """
        计算因子的命中率。命中率是组合平均每个月跑赢基准的行业占比
        """
        hitrate_by_day = self.factor_data_ex.groupby(["Factor_quantile", "Date"])["Forward_1"].apply(lambda x: (x > 0).sum() / x.count())
        
        # 整体表现
        hitrate = hitrate_by_day.groupby(["Factor_quantile"]).mean()
        
        # 分年分组表现
        grouper = [hitrate_by_day.index.get_level_values(1).year]
        hitrate_by_year = hitrate_by_day.groupby(grouper).mean()

        return hitrate, hitrate_by_year

    def stats_decay_by_group(self):
        """
        计算因子的衰减率。接下去第一个月、第二个月、第三个月直到第十二个月的超额收益率
        """
        alpha_by_date = self.factor_data_ex.groupby(["Date", "Factor_quantile"]).sum().drop(columns=["Factor"]) # 每期每组的未来收益率
        alpha_by_date.replace(0, np.nan, inplace=True) # 将0替换为nan
        alpha = alpha_by_date.groupby(["Factor_quantile"]).mean() 
        alpha.columns = [f"M{i}" for i in range(1, 13)]
        return alpha
    
    # ------------------------ 详细情况 -----------------------------------------
    def stats_asset_in_detail_by_year(self):
        """每个组每年选中的资产及其命中率"""
        grouper = ["Factor_quantile", self.factor_data_ex.index.get_level_values(0).year, "Asset"] # 按照组别、年份、资产分组
        
        # 累计超额、选中次数、命中次数、命中率
        asset_ex_by_year = self.factor_data_ex.groupby(grouper).Forward_1.agg(["sum", "count", lambda x: (x>0).sum(), lambda x: (x>0).sum()/x.count()]).dropna()
        
        # 因子均值
        asset_factor_by_year = self.factor_data_ex.groupby(grouper).Factor.mean()
        
        # 合并
        asset_ex_by_year = asset_ex_by_year.join(asset_factor_by_year)
        asset_ex_by_year.columns = ["累计超额", "选中次数", "命中次数", "命中率", "因子均值"]
        
        asset_ex_by_year = asset_ex_by_year[["因子均值", "累计超额", "选中次数", "命中次数", "命中率"]].reset_index()

        # 加入板块数据
        if self.sector_data is not None:
            if self.asset_type == "industry": # 如果是行业，则加入板块数据；如果是股票，不能做到一一匹配，因为所属板块会随时间变化
                asset_ex_by_year = self.merge_asset_and_sector(asset_ex_by_year)
        return asset_ex_by_year

    def stats_sector_in_detail_by_year(self):
        """每组每年选中的板块及其命中率, 板块收益率是板块内行业收益率的平均, 相当于等权配置"""
        asset_ex_by_year = self.stats_asset_in_detail_by_year()
        sector_ex_by_year = asset_ex_by_year.groupby(["Factor_quantile", "Date", "Sector"]).agg({"因子均值": "mean", "累计超额": "sum", "选中次数": "sum", "命中次数": "sum", "命中率": "mean"}).dropna()
        return sector_ex_by_year.reset_index()

    def stats_asset_group_score(self):
        """资产组合平均得分, 被分到G1得1分, 分到G5得5分, 分到G10得10分"""
        tmp = self.factor_data.Factor_quantile.apply(lambda x: x[1:]).dropna().astype(np.int).groupby(["Asset"]).mean().sort_values(ascending=False)
        tmp = tmp.reset_index()
        tmp.columns = ["Asset", "Score"]

        if self.sector_data is not None:
            if self.asset_type == "industry": # 如果是行业，则加入板块数据；如果是股票，不能做到一一匹配，因为所属板块会随时间变化
                tmp = self.merge_asset_and_sector(tmp)
        return tmp
    
    # -------------------------- 保存结果 --------------------------------------
    def plot_factortrend_of_asset(self, asset="IT服务"):
        # 净值
        nav = self.factor_data.query(f"Asset=='{asset}'")["Forward_1"].droplevel(1).cumsum()
        # 因子
        factor = self.factor_data.query(f"Asset=='{asset}'")["Factor"].droplevel(1)
        # 分组
        group = self.factor_data.query(f"Asset=='{asset}'")["Factor_quantile"].droplevel(1)
        
        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
        ax2 = ax.twinx()
        nav.plot(ax=ax, label="NAV") # 净值走势
        factor.plot(ax=ax2, color="#fdae61", alpha=0.5, label="factor") # 因子走势

        for date in group[group==self.quantile_labels[0]].index:
            xmin = date
            xmax = group.loc[date:].iloc[:2].index[-1]
            ax.axvspan(xmin=xmin, xmax=xmax, facecolor="#abdda4", alpha=0.3)

        for date in group[group==self.quantile_labels[-1]].index:
            xmin = date
            xmax = group.loc[date:].iloc[:2].index[-1]
            ax.axvspan(xmin=xmin, xmax=xmax, facecolor="#d7191c", alpha=0.1)

        ax.set_title(f"{asset}-因子和净值趋势")

        fig.legend()
        
        return nav, factor, group, fig
    
    def save_detailed_result(self, save_path=None):
        if save_path is None:
            save_path = "详细结果.xlsx"
            
        with pd.ExcelWriter(
            save_path,
            datetime_format='YYYY-MM-DD'  # 只显示年月日, 不显示时分秒
        ) as writer:
            if self.sector_data is not None:
                self.factor_IC_stats(by_sector=True).to_excel(writer, sheet_name="IC统计量")
                self.factor_IC_cum(by_sector=True).to_excel(writer, sheet_name="累计IC")
                
                self.excess_nav_by_group(by_sector=False).dropna().to_excel(writer, sheet_name="分组超额净值")
                self.excess_nav_by_group(by_sector=True).dropna().to_excel(writer, sheet_name="分板块-分组超额净值")
                
                alpha, alpha_by_year = self.stats_alpha_by_group(by_sector=False)
                alpha_by_month = self.stats_alpha_by_group_and_month(by_sector=False)
                winrate, winrate_by_year = self.stats_winrate_by_group()
                hitrate, hitrate_by_year = self.stats_hitrate_by_group()
                result = pd.concat([alpha, winrate, hitrate], axis=1)
                result.columns = ["超额收益率", "胜率", "命中率"]
                result.to_excel(writer, sheet_name="分年分组汇总")
                alpha_by_year.to_excel(writer, sheet_name="分年分组超额")
                alpha_by_month.to_excel(writer, sheet_name="分月分组超额")
                
                alpha, alpha_by_year = self.stats_alpha_by_group(by_sector=True)
                alpha_by_year = alpha_by_year.replace(0, np.nan).dropna()
                alpha_by_year.to_excel(writer, sheet_name="分板块-分年分组超额")
                
                # 衰减情况
                self.stats_decay_by_group().to_excel(writer, sheet_name="衰减")
                self.factor_IC_decay().to_frame().rename(columns={0: "IC 衰减"}).T.to_excel(writer, sheet_name="衰减", startrow=self.quantile+3)
                
                # 明细情况
                self.stats_asset_group_score().to_excel(writer, sheet_name="资产组别得分", index=False)
                self.stats_asset_in_detail_by_year().to_excel(writer, sheet_name="资产情况明细-分年", index=False)
                self.stats_sector_in_detail_by_year().to_excel(writer, sheet_name="板块情况明细-分年", index=False)
                
            else:
                self.factor_IC_stats(by_sector=False).to_excel(writer, sheet_name="IC统计量")
                self.factor_IC_cum(by_sector=False).to_excel(writer, sheet_name="累计IC")
                self.excess_nav_by_group(by_sector=False).dropna().to_excel(writer, sheet_name="分组超额净值")
                alpha, alpha_by_year = self.stats_alpha_by_group(by_sector=False)
                alpha_by_month = self.stats_alpha_by_group_and_month(by_sector=False)
                winrate, winrate_by_year = self.stats_winrate_by_group()
                hitrate, hitrate_by_year = self.stats_hitrate_by_group()
                result = pd.concat([alpha, winrate, hitrate], axis=1)
                result.columns = ["超额收益率", "胜率", "命中率"]
                result.to_excel(writer, sheet_name="分年分组汇总")
                alpha_by_year.to_excel(writer, sheet_name="分年分组超额")
                alpha_by_month.to_excel(writer, sheet_name="分月分组超额")
                # 衰减情况
                self.stats_decay_by_group().to_excel(writer, sheet_name="衰减")
                self.factor_IC_decay().to_frame().rename(columns={0: "IC 衰减"}).T.to_excel(writer, sheet_name="衰减", startrow=self.quantile+3)
                
                # 明细情况
                self.stats_asset_group_score().to_excel(writer, sheet_name="资产组别得分", index=False)
                self.stats_asset_in_detail_by_year().to_excel(writer, sheet_name="资产情况明细-分年", index=False)

        print(f"因子测试的详细结果已保存到 {save_path}")
        