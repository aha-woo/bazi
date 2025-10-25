"""
八字计算核心算法
支持：阳历转农历、天干地支计算、四柱推算、五行分析
"""
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Tuple


class BaziCalculator:
    """八字计算器"""
    
    # 天干
    TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支
    DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 五行
    WUXING = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水',
        '子': '水', '丑': '土', '寅': '木', '卯': '木',
        '辰': '土', '巳': '火', '午': '火', '未': '土',
        '申': '金', '酉': '金', '戌': '土', '亥': '水'
    }
    
    # 十神关系
    SHISHEN = {
        '比肩': '同我', '劫财': '同我',
        '食神': '我生', '伤官': '我生',
        '偏财': '我克', '正财': '我克',
        '七杀': '克我', '正官': '克我',
        '偏印': '生我', '正印': '生我'
    }
    
    # 五行相生相克
    WUXING_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
    WUXING_KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
    
    @staticmethod
    def calculate_ganzhi_year(year: int) -> str:
        """计算年柱天干地支"""
        # 1984年是甲子年（天干和地支都从0开始）
        base_year = 1984
        year_offset = year - base_year
        
        tian_index = year_offset % 10
        di_index = year_offset % 12
        
        return BaziCalculator.TIANGAN[tian_index] + BaziCalculator.DIZHI[di_index]
    
    @staticmethod
    def calculate_ganzhi_month(year: int, month: int, day: int) -> str:
        """计算月柱天干地支"""
        # 调整月份（立春为岁首）
        # 简化处理：2月4日前算前一年
        if month == 1 or (month == 2 and day < 4):
            year -= 1
            month += 12
        
        # 月份地支：寅月（正月）开始
        # 1月=寅(2), 2月=卯(3), ..., 12月=丑(1)
        month_dizhi_index = (month + 1) % 12
        
        # 月干由年干推算：甲己之年丙作首
        year_tian = (year - 4) % 10
        month_tian_base = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
        month_tian_index = (month_tian_base[year_tian] + month - 1) % 10
        
        return BaziCalculator.TIANGAN[month_tian_index] + BaziCalculator.DIZHI[month_dizhi_index]
    
    @staticmethod
    def calculate_ganzhi_day(date: datetime) -> str:
        """计算日柱天干地支"""
        # 使用已知的基准日期：2000年1月1日是戊午日
        base_date = datetime(2000, 1, 1)
        base_tian = 4  # 戊
        base_di = 6    # 午
        
        days_diff = (date - base_date).days
        
        tian_index = (base_tian + days_diff) % 10
        di_index = (base_di + days_diff) % 12
        
        return BaziCalculator.TIANGAN[tian_index] + BaziCalculator.DIZHI[di_index]
    
    @staticmethod
    def calculate_ganzhi_hour(hour: int, day_tian: str) -> str:
        """计算时柱天干地支"""
        # 时辰地支
        hour_dizhi_map = {
            23: 0, 0: 0,  # 子时
            1: 1, 2: 1,   # 丑时
            3: 2, 4: 2,   # 寅时
            5: 3, 6: 3,   # 卯时
            7: 4, 8: 4,   # 辰时
            9: 5, 10: 5,  # 巳时
            11: 6, 12: 6, # 午时
            13: 7, 14: 7, # 未时
            15: 8, 16: 8, # 申时
            17: 9, 18: 9, # 酉时
            19: 10, 20: 10, # 戌时
            21: 11, 22: 11  # 亥时
        }
        
        hour_di_index = hour_dizhi_map.get(hour, 0)
        
        # 时干由日干推算：甲己还加甲
        day_tian_index = BaziCalculator.TIANGAN.index(day_tian)
        hour_tian_base = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
        hour_tian_index = (hour_tian_base[day_tian_index] + hour_di_index) % 10
        
        return BaziCalculator.TIANGAN[hour_tian_index] + BaziCalculator.DIZHI[hour_di_index]
    
    @staticmethod
    def calculate_bazi(birth_datetime: datetime, timezone_str: str = 'Asia/Shanghai') -> Dict:
        """
        计算八字四柱
        
        Args:
            birth_datetime: 出生时间（UTC或本地时间）
            timezone_str: 时区字符串
            
        Returns:
            包含四柱、五行等信息的字典
        """
        # 转换到指定时区
        if birth_datetime.tzinfo is None:
            tz = pytz.timezone(timezone_str)
            birth_datetime = tz.localize(birth_datetime)
        else:
            tz = pytz.timezone(timezone_str)
            birth_datetime = birth_datetime.astimezone(tz)
        
        year = birth_datetime.year
        month = birth_datetime.month
        day = birth_datetime.day
        hour = birth_datetime.hour
        
        # 计算四柱
        year_ganzhi = BaziCalculator.calculate_ganzhi_year(year)
        month_ganzhi = BaziCalculator.calculate_ganzhi_month(year, month, day)
        day_ganzhi = BaziCalculator.calculate_ganzhi_day(birth_datetime)
        hour_ganzhi = BaziCalculator.calculate_ganzhi_hour(hour, day_ganzhi[0])
        
        # 提取天干地支
        sizhu = {
            'year': {'ganzhi': year_ganzhi, 'tian': year_ganzhi[0], 'di': year_ganzhi[1]},
            'month': {'ganzhi': month_ganzhi, 'tian': month_ganzhi[0], 'di': month_ganzhi[1]},
            'day': {'ganzhi': day_ganzhi, 'tian': day_ganzhi[0], 'di': day_ganzhi[1]},
            'hour': {'ganzhi': hour_ganzhi, 'tian': hour_ganzhi[0], 'di': hour_ganzhi[1]}
        }
        
        # 分析五行
        wuxing_count = BaziCalculator.analyze_wuxing(sizhu)
        
        # 获取日主（命主）
        rigan = day_ganzhi[0]
        rigan_wuxing = BaziCalculator.WUXING[rigan]
        
        return {
            'birth_time': birth_datetime.isoformat(),
            'timezone': timezone_str,
            'sizhu': sizhu,
            'year_pillar': year_ganzhi,
            'month_pillar': month_ganzhi,
            'day_pillar': day_ganzhi,
            'hour_pillar': hour_ganzhi,
            'rigan': rigan,
            'rigan_wuxing': rigan_wuxing,
            'wuxing_analysis': wuxing_count
        }
    
    @staticmethod
    def analyze_wuxing(sizhu: Dict) -> Dict:
        """分析八字中的五行分布"""
        wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
        
        for pillar in ['year', 'month', 'day', 'hour']:
            tian = sizhu[pillar]['tian']
            di = sizhu[pillar]['di']
            
            wuxing_count[BaziCalculator.WUXING[tian]] += 1
            wuxing_count[BaziCalculator.WUXING[di]] += 1
        
        # 找出最旺和最弱的五行
        max_wuxing = max(wuxing_count, key=wuxing_count.get)
        min_wuxing = min(wuxing_count, key=wuxing_count.get)
        
        return {
            'count': wuxing_count,
            'strongest': max_wuxing,
            'weakest': min_wuxing,
            'total': sum(wuxing_count.values())
        }
    
    @staticmethod
    def get_interpretation(bazi_data: Dict) -> Dict:
        """
        生成命理解读
        
        Args:
            bazi_data: 八字数据
            
        Returns:
            命理解读信息
        """
        rigan = bazi_data['rigan']
        rigan_wuxing = bazi_data['rigan_wuxing']
        wuxing = bazi_data['wuxing_analysis']
        
        # 基础解读
        basic_interpretation = f"您的日主为{rigan}，五行属{rigan_wuxing}。"
        
        # 五行分析
        wuxing_text = "您的八字中，"
        for wx, count in wuxing['count'].items():
            wuxing_text += f"{wx}有{count}个，"
        wuxing_text = wuxing_text.rstrip('，') + "。"
        
        # 五行旺衰
        balance_text = f"五行中{wuxing['strongest']}最旺，{wuxing['weakest']}最弱。"
        
        # 性格特征（基于日主）
        personality = BaziCalculator.get_personality_by_rigan(rigan)
        
        # 喜用神建议
        xiyongshen = BaziCalculator.get_xiyongshen(rigan_wuxing, wuxing['count'])
        
        # 运势建议
        advice = BaziCalculator.get_advice(rigan_wuxing, wuxing)
        
        return {
            'basic': basic_interpretation,
            'wuxing_distribution': wuxing_text,
            'wuxing_balance': balance_text,
            'personality': personality,
            'xiyongshen': xiyongshen,
            'advice': advice,
            'full_text': f"{basic_interpretation}\n\n{wuxing_text}{balance_text}\n\n【性格特征】\n{personality}\n\n【喜用神】\n{xiyongshen}\n\n【建议】\n{advice}"
        }
    
    @staticmethod
    def get_personality_by_rigan(rigan: str) -> str:
        """根据日主分析性格特征"""
        personalities = {
            '甲': "甲木日主，如参天大树，性格刚直，有向上的进取心，富有正义感。做事积极主动，但有时过于倔强。",
            '乙': "乙木日主，如花草藤蔓，性格柔和，善于适应环境，心思细腻。为人亲切温和，但有时显得优柔寡断。",
            '丙': "丙火日主，如太阳之火，性格热情开朗，充满活力，善于表达。做事光明磊落，但有时过于冲动。",
            '丁': "丁火日主，如灯烛之火，性格温和细腻，内心热情，善于思考。为人谨慎周到，但有时过于敏感。",
            '戊': "戊土日主，如高山厚土，性格稳重可靠，包容力强，诚实守信。做事踏实，但有时过于固执。",
            '己': "己土日主，如田园之土，性格温和谦逊，善于协调，注重实际。为人和善，但有时过于保守。",
            '庚': "庚金日主，如刚铁利剑，性格刚毅果断，有魄力和决断力。做事干脆利落，但有时过于刚硬。",
            '辛': "辛金日主，如珠玉首饰，性格细腻敏锐，追求完美，有审美品味。为人精致，但有时过于挑剔。",
            '壬': "壬水日主，如江河之水，性格灵活变通，智慧聪明，善于交际。思维活跃，但有时过于多变。",
            '癸': "癸水日主，如雨露甘泉，性格温柔细腻，内敛深沉，富有想象力。为人含蓄，但有时过于敏感。"
        }
        return personalities.get(rigan, "性格随和，为人处世有自己的特点。")
    
    @staticmethod
    def get_xiyongshen(rigan_wuxing: str, wuxing_count: Dict) -> str:
        """推算喜用神"""
        # 简化算法：根据五行平衡推算
        weak_elements = [wx for wx, count in wuxing_count.items() if count <= 1]
        strong_elements = [wx for wx, count in wuxing_count.items() if count >= 3]
        
        if not weak_elements:
            return f"您的八字五行较为平衡，日常可多接触{rigan_wuxing}相关的事物。"
        
        # 找出能生助弱五行的元素
        xiyong = []
        for weak in weak_elements:
            for element, sheng in BaziCalculator.WUXING_SHENG.items():
                if sheng == weak and element not in strong_elements:
                    xiyong.append(element)
        
        if xiyong:
            return f"根据您的八字，建议以{', '.join(set(xiyong))}为喜用神，可在生活中多接触相关颜色、方位、职业等。"
        else:
            return f"建议以{weak_elements[0]}为喜用神，可在生活中多接触{weak_elements[0]}相关的事物。"
    
    @staticmethod
    def get_advice(rigan_wuxing: str, wuxing_analysis: Dict) -> str:
        """给出运势建议"""
        strongest = wuxing_analysis['strongest']
        weakest = wuxing_analysis['weakest']
        
        advice = []
        
        # 颜色建议
        color_map = {
            '木': '绿色、青色',
            '火': '红色、紫色',
            '土': '黄色、棕色',
            '金': '白色、金色',
            '水': '黑色、蓝色'
        }
        advice.append(f"颜色方面：可多穿戴{color_map[weakest]}系的衣物，有助于平衡五行。")
        
        # 方位建议
        direction_map = {
            '木': '东方',
            '火': '南方',
            '土': '中央',
            '金': '西方',
            '水': '北方'
        }
        advice.append(f"方位方面：{direction_map[weakest]}为您的有利方位。")
        
        # 职业建议
        career_map = {
            '木': '文教、医疗、林业、纺织',
            '火': '能源、娱乐、餐饮、电子',
            '土': '房地产、建筑、农业、管理',
            '金': '金融、机械、科技、法律',
            '水': '贸易、物流、旅游、通讯'
        }
        advice.append(f"事业方面：适合从事{career_map[rigan_wuxing]}相关行业。")
        
        return '\n'.join(advice)


def calculate_bazi_from_input(
    year: int, 
    month: int, 
    day: int, 
    hour: int, 
    minute: int = 0,
    timezone_str: str = 'Asia/Shanghai'
) -> Dict:
    """
    从用户输入计算八字
    
    Args:
        year: 年份
        month: 月份 (1-12)
        day: 日期 (1-31)
        hour: 小时 (0-23)
        minute: 分钟 (0-59)
        timezone_str: 时区
        
    Returns:
        完整的八字分析结果
    """
    birth_datetime = datetime(year, month, day, hour, minute)
    bazi_data = BaziCalculator.calculate_bazi(birth_datetime, timezone_str)
    interpretation = BaziCalculator.get_interpretation(bazi_data)
    
    return {
        **bazi_data,
        'interpretation': interpretation
    }

