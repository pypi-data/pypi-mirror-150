导入 xlwings 为 xw
从 汉化通用 导入 _关键词参数中转英, _反向注入

套路 查看(对象, 工作表=空, 表=真, 块大小=5000):
    '''
    打开一个新工作簿并显示 '对象', 默认显示在第一张工作表上.
    如果指定工作表, 则显示对象之前会清除现有工作表上的内容.

    '对象' 参数可以是数字、字符串、列表、数王 (numpy) 数组、熊猫 (pandas) 数据帧等.

    示例
    -------------

    导入 格子 \n
    数据 = [['1月', '2月', '3月'], [1, 2, 3]] \n
    格子.查看(数据)
    '''
    xw.view(对象, sheet=工作表, table=表, chunksize=块大小)

套路 加载(索引=1, 表头=1, 块大小=5000):
    """将活动工作簿的选定单元格加载到 pandas 数据帧中.

    仅用于 jupyter notebook 等交互环境.
    """
    返回 xw.load(index=索引, header=表头, chunksize=块大小)


xw.main.Collection.计数 = xw.main.Collection.count
〇组合 = xw.main.Collection

xw.main.Apps.键々 = xw.main.Apps.keys
xw.main.Apps.活动应用 = xw.main.Apps.active
xw.main.Apps.计数 = xw.main.Apps.count

套路 __新建(分身, **关键词参数):
    '''
    新建一个应用, 新应用成为活动应用.
    '''
    返回 分身.add(**关键词参数)

xw.main.Apps.新建 = __新建


类 〇应用(xw.App):
    '''
    一个应用就是一个 Excel 实例.

    示例
    ---------
    导入 格子 \n
    应用1 = 格子.〇应用() \n
    应用2 = 格子.〇应用() \n
    格子.应用々 \n
    > 应用々([<Excel App 1668>, <Excel App 1644>]) \n
    格子.应用々[1668] # 1668 等是进程 ID (PID), 可通过 格子.应用々.键々() 获得 \n
    > <Excel 应用 1668> \n
    格子.应用々.活动应用 \n
    > <Excel 应用 1668>

    参数
    ---------
    可见 : 布尔值, 决定应用是否可见, 默认可见

    规格 : 字符串, 默认为 空. 若要改变与斑马交互的 Excel 应用程序和/或版本, 在 Windows
    上需要到控制面板里面修改默认值, 在 Mac 上需要将完整路径赋给 <规格> 参数.
    '''
    套路 __init__(分身, 可见=空, 规格=空, 添加工作簿=真, impl=空):
        super().__init__(visible=可见, spec=规格, add_book=添加工作簿, impl=impl)
        分身.版本 = 分身.version
        分身.引擎 = 分身.engine
        分身.启动路径 = 分身.startup_path
    
    @property
    套路 选定单元格(分身) -> '〇范围':
        '''
        将选定单元格作为 <〇范围> 对象返回.
        '''
        返回 〇范围(impl=分身.impl.selection) 如果 分身.impl.selection 否则 空

    套路 激活(分身, 偷焦点=假):
        '''
        激活 Excel 应用.
        如果 <偷焦点> 为真, 则焦点从草蟒转移给 Excel.
        '''
        分身.activate(偷焦点)
    
    @property
    套路 可见(分身):
        '''获取或设置 Excel 的可见性'''
        返回 分身.visible

    @可见.setter
    套路 可见(分身, 值):
        分身.visible = 值

    套路 退出(分身):
        '''
        退出应用程序而不保存工作簿.
        '''
        返回 分身.quit()

    套路 杀死(分身):
        '''
        杀死 Excel 应用进程, 强制其退出.
        '''
        返回 分身.kill()

    @property
    套路 屏幕更新(分身):
        '''
        关闭屏幕更新可加速脚本执行.
        记住脚本结束之后将此属性设置为 <真>.
        '''
        返回 分身.screen_updating

    @屏幕更新.setter
    套路 屏幕更新(分身, 值):
        分身.screen_updating = 值

    @property
    套路 显示告警(分身):
        '''
        默认值为真. 若将此属性设置为假,
        则代码执行时不显示提示和警报.
        '''
        返回 分身.display_alerts

    @显示告警.setter
    套路 显示告警(分身, 值):
        分身.display_alerts = 值
    
    @property
    套路 启用事件(分身):
        '''
        若启用事件则为真
        '''
        返回 分身.enable_events

    @启用事件.setter
    套路 启用事件(分身, 值):
        分身.enable_events = 值
    
    @property
    套路 交互模式(分身):
        '''
        若处于交互模式则为真
        '''
        返回 分身.interactive

    @交互模式.setter
    套路 交互模式(分身, 值):
        分身.interactive = 值
    
    @property
    套路 计算模式(分身):
        '''
        返回或设置计算模式:
        '手动', '自动', '半自动'

        示例
        --------

        导入 格子 \n
        工作簿 = 格子.〇工作簿() \n
        工作簿.应用.计算模式 = '手动'
        '''
        取计算模式字典 = {
            'manual':'手动', 
            'automatic':'自动', 
            'semiautomatic':'半自动'
        }
        返回 取计算模式字典[分身.calculation]

    @计算模式.setter
    套路 计算模式(分身, 值):
        设计算模式字典 = {
            '手动':'manual', 
            '自动':'automatic', 
            '半自动':'semiautomatic'
        }
        分身.calculation = 设计算模式字典.获取(值, 值)

    套路 计算(分身):
        '''
        计算所有打开的工作簿.'''
        分身.calculate()

    @property
    套路 工作簿々(分身) -> '〇工作簿々':
        '''
        当前打开的所有工作簿对象的集合.
        '''
        返回 〇工作簿々(impl=分身.impl.books)

    @property
    套路 窗口句柄(分身):
        '''
        仅限 Windows 系统.
        '''
        返回 分身.hwnd

    @property
    套路 进程id(分身):
        '''
        仅限 Windows 系统.
        '''
        返回 分身.pid

    套路 范围(分身, 单元格1, 单元格2=空) -> '〇范围':
        '''
        返回活动工作簿的活动工作表中的范围对象.
        '''
        返回 〇范围(impl=分身.impl.range(cell1, cell2))

    套路 __repr__(分身):
        返回 "<Excel 应用 %s>" % 分身.pid

    套路 宏(分身, 名称):
        '''
        运行 Excel VBA 中的 Sub 或 Function
        '''
        返回 〇宏(分身, 名称)

    @property
    套路 状态栏(分身):
        '''
        获取或设置状态栏的值.
        '''
        返回 分身.status_bar

    @状态栏.setter
    套路 状态栏(分身, 值):
        分身.status_bar = 值
    
    @property
    套路 剪切复制模式(分身):
        '''
        获取或设置剪切或复制模式的状态.
        '''
        返回 分身.cut_copy_mode

    @剪切复制模式.setter
    套路 剪切复制模式(分身, 值):
        分身.cut_copy_mode = 值

    套路 属性々(分身, **关键词参数):
        返回 分身.properties(**关键词参数)

    套路 渲染模板(分身, 模板=空, 输出=空, 工作簿设置=空, **数据):
        返回 分身.render_template(template=模板, output=输出, book_settings=工作簿设置, **数据)

_反向注入(〇应用, xw.App)


类 〇工作簿(xw.Book):
    '''
    工作簿类对象
    
    示例
    ---------

    导入 格子 \n
    格子.工作簿々[0] \n
    > <工作簿 [测试.xlsx]>

    新建工作簿 : ``格子.〇工作簿()`` , ``格子.工作簿々.新建()`` \n
    连接到未保存的工作簿 : ``格子.〇工作簿('测试.xlsx')`` , ``格子.工作簿々['测试.xlsx']`` \n
    通过全名连接工作簿 : ``格子.〇工作簿(r'C:/Users/Administrator/Desktop/测试.xlsx')`` ,
    ``格子.工作簿々[r'C:/Users/Administrator/Desktop/测试.xlsx']`` \n
    
    参数
    ---------

    说明待补充
    '''

    套路 __init__(分身, 全名=空, 更新链接=空, 只读=空, 格式=空, 密码=空, 写保护密码=空,
                忽略只读建议=空, 来源=空, 分界符=空, 可编辑=空, 通知=空, 转换器=空, 
                添加到最近使用列表=空, 本地=空, 损坏加载=空, impl=空, json=空):
        super().__init__(fullname=全名, update_links=更新链接, read_only=只读, 
                format=格式, password=密码, write_res_password=写保护密码,
                ignore_read_only_recommended=忽略只读建议, origin=来源, delimiter=分界符, 
                editable=可编辑, notify=通知, converter=转换器, 
                add_to_mru=添加到最近使用列表, local=本地, corrupt_load=损坏加载,
                impl=impl, json=json)

    # caller()
    # set_mock_caller()

    套路 宏(分身, 名称):
        '''
        运行 Excel VBA 中的 Sub 或 Function.
        '''
        返回 分身.macro(名称)

    @property
    套路 名称(分身):
        '''返回工作簿的名称'''
        返回 分身.name

    @property
    套路 工作表々(分身) -> '〇工作表々':
        '''返回工作簿中所有工作表的集合'''
        返回 〇工作表々(impl=分身.impl.sheets)

    @property
    套路 应用(分身):
        '''返回创建工作簿的应用对象'''
        返回 〇应用(impl=分身.impl.app)

    套路 关闭(分身):
        '''关闭工作簿而不保存'''
        分身.close()

    套路 保存(分身, 路径=空):
        '''保存工作簿'''
        返回 分身.save(路径)

    @property
    套路 全名(分身):
        '''返回对象的名称, 包括磁盘路径'''
        返回 分身.fullname

    @property
    套路 名称々(分身) -> '〇名称々':
        '''返回指定工作簿中所有名称的集合'''
        返回 〇名称々(impl=分身.impl.names)

    套路 激活(分身, 偷焦点=假):
        '''
        激活工作簿.
        如果 <偷焦点> 为真, 则焦点从草蟒转移给 Excel.
        '''
        分身.activate(偷焦点)

    @property
    套路 选定单元格(分身) -> '〇范围':
        '''
        将选定单元格作为 <〇范围> 对象返回.
        '''
        返回 〇范围(impl=分身.app.selection.impl) 如果 分身.app.selection 否则 空

    套路 转为pdf(分身, 路径=空, 包括=空, 排除=空, 布局=空, 排除起始字符串="#",
                显示=假, 质量="标准"):
        如果 质量 == "标准":
            质量 = "standard"
        或如 质量 == "最低":
            质量 = "minimum"

        返回 分身.to_pdf(
            path=路径,
            include=包括,
            exclude=排除,
            layout=布局,
            exclude_start_string=排除起始字符串,
            show=显示,
            quality=质量,
        )

    套路 __repr__(分身):
        返回 "<工作簿 [{0}]>".格式化(分身.name)

    套路 渲染模板(分身, **数据):
        分身.render_template(**数据)

_反向注入(〇工作簿, xw.Book)

类 〇工作表(xw.Sheet):
    '''
    工作表类对象.

    导入 格子 \n
    格子.工作表々[0] \n
    > <工作表 [测试.xlsx]Sheet1> \n
    格子.工作表々.新建() \n
    > <工作表 [测试.xlsx]Sheet4>
    '''
    套路 __init__(分身, 工作表=空, impl=空):
        super().__init__(sheet=工作表, impl=impl)

    @property
    套路 名称(分身):
        '''获取或设置工作表的名称'''
        返回 分身.name

    @名称.setter
    套路 名称(分身, 值):
        分身.name = 值

    @property
    套路 名称々(分身) -> '〇名称々': # 中文英文似乎都返回空列表?
        '''返回工作表特定的所有名称的集合'''
        返回 〇名称々(impl=分身.impl.names)

    @property
    套路 工作簿(分身) -> '〇工作簿':
        '''返回指定工作表所属的工作簿'''
        返回 〇工作簿(impl=分身.impl.book)

    @property
    套路 索引(分身):
        '''返回工作表的索引 (从 1 开始)'''
        返回 分身.index

    套路 范围(分身, 单元格1, 单元格2=空) -> '〇范围':
        '''
        返回活动工作簿的活动工作表中的范围对象.
        '''
        如果 是实例(单元格1, xw.Range):
            如果 单元格1.sheet != 分身:
                报 值错误类("第一个范围不在此工作表上")
            单元格1 = 单元格1.impl
        如果 是实例(单元格2, xw.Range):
            如果 单元格2.sheet != 分身:
                报 值错误类("第二个范围不在此工作表上")
            单元格2 = 单元格2.impl
        返回 〇范围(impl=分身.impl.range(单元格1, 单元格2))

    @property
    套路 单元格々(分身) -> '〇范围':
        '''返回一个代表工作表上所有单元格的范围对象'''
        返回 〇范围(impl=分身.impl.cells)

    套路 激活(分身):
        '''激活工作表并返回该对象'''
        分身.activate() # 原库说会返回工作表, 但实际上是 None, 所以这里不用 <返回>

    套路 选中(分身):
        '''选中工作表, 仅对活动工作簿有效'''
        返回 分身.select()

    套路 清除内容(分身):
        '''清除整个工作表的内容, 但保留格式'''
        返回 分身.clear_contents()
    
    套路 清除格式(分身):
        '''清除整个工作表的格式, 但保留内容'''
        返回 分身.clear_formats()

    套路 清空(分身):
        '''清除整个工作表的内容和格式'''
        返回 分身.clear()

    套路 自适应(分身, 轴=空):
        '''自适应整个工作表的行高和/或列宽.\n
        如果仅要求行高自适应, 请指定: 轴="行".\n
        如果仅要求列宽自适应, 请指定: 轴="列".\n
        如果要同时适应, 请勿指定该参数.
        '''
        如果 轴 == '行':
            轴 = 'r'
        或如 轴 == '列':
            轴 = 'c'
        返回 分身.autofit(轴)

    套路 删除(分身):
        '''删除工作表'''
        返回 分身.delete()

    套路 转为pdf(分身, 路径=空, 布局=空, 显示=假, 质量="标准"):
        如果 质量 == "标准":
            质量 = "standard"
        或如 质量 == "最低":
            质量 = "minimum"
        返回 分身.to_pdf(path=路径, layout=布局, show=显示, quality=质量)

    套路 __repr__(分身):
        返回 "<工作表 [{1}]{0}>".格式化(分身.name, 分身.book.name)

    套路 复制(分身, 之前=空, 之后=空, 名称=空):
        """将一个工作表复制到当前或新工作簿.
        """
        返回 分身.copy(before=之前, after=之后, name=名称)

    套路 渲染模板(分身, **数据):
        分身.render_template(**数据)

    @property
    套路 图表々(分身) -> '〇图表々':
        '''返回指定工作表上所有图表对象的集合'''
        返回 〇图表々(impl=分身.impl.charts)

    @property
    套路 形状々(分身) -> '〇形状々':
        '''返回指定工作表上所有形状对象的集合'''
        返回 〇形状々(impl=分身.impl.shapes)

    @property
    套路 图片々(分身) -> '〇图片々':
        '''返回指定工作表上所有图片对象的集合'''
        返回 〇图片々(impl=分身.impl.pictures)
    
    @property
    套路 表々(分身) -> '〇表々':
        '''返回指定工作表上所有表对象的集合'''
        返回 〇表々(impl=分身.impl.tables)

    套路 已用范围(分身) -> '〇范围':
        '''工作表已使用的范围'''
        返回 〇范围(impl=分身.impl.used_range)

    @property
    套路 可见(分身):
        '''获取或设置工作表的可见性'''
        返回 分身.visible

    @可见.setter
    套路 可见(分身, 值):
        分身.visible = 值

    @property
    套路 页面设置(分身):
        '''返回一个页面设置对象'''
        返回 分身.page_setup

_反向注入(〇工作表, xw.Sheet)


类 〇范围(xw.Range):
    """
    返回一个范围对象, 它可代表一个单元格或一系列单元格.

    示例
    --------

    对于活动工作表: \n
    导入 格子 \n
    格子.〇范围('A1')  # 用小写字母也可以, 比如 'a1' \n
    格子.〇范围('A1:C3') \n
    格子.〇范围((1,1)) \n
    格子.〇范围((1,1), (3,3)) \n
    格子.〇范围('价格')  # '价格' 是工作表中已定义的一个名称, 代表某个范围 \n
    格子.〇范围(格子.〇范围('A1'), 格子.〇范围('B2')) \n

    对于特定工作表: \n
    格子.工作簿々['测试.xlsx'].工作表々[0].〇范围('A1')

    """
    套路 __init__(分身, 单元格1=空, 单元格2=空, **选项々):
        xw.Range.__init__(分身, cell1=单元格1, cell2=单元格2, **选项々)

    套路 选项々(分身, 转换=空, **选项々) -> '〇范围':
        '''
        用于设置转换器及其选项，返回范围对象. \n
        转换器定义读写操作中如何转换 Excel 范围及其值.
        '''
        选项字典 = {
            '维数' : 'ndim', # 维数
            '数字类型' : 'numbers', # 例如 <整数>
            '日期类型' : 'dates', # 默认为 <日期时间.日期时间>
            '空单元格' : 'empty', # 可指定 'NA' 等, 默认为 None/空
            '转置' : 'transpose', # 真/假
            '扩展' : 'expand',
        }
        选项值字典 = {
            '表格' : 'table', # <扩展> 选项々
            '向下' : 'down',
            '向右' : 'right',
            '整数' : 'int',
        }
        选项々 = _关键词参数中转英(选项々, 选项字典, 选项值字典)
        选项々['convert'] = 转换
        返回 〇范围(
            impl=分身.impl,
            **选项々
        )

    套路 转置(分身):
        '''将值从横向填充转变为纵向填充'''
        返回 分身.选项々(transpose=True)

    @property
    套路 工作表(分身) -> '〇工作表':
        '''返回范围所属的工作表对象'''
        返回 〇工作表(impl=分身.impl.sheet)

    @property
    套路 计数(分身):
        '''返回单元格数目'''
        返回 长(分身)
    
    @property
    套路 行号(分身):
        '''返回指定范围第一行的序号, 只读'''
        返回 分身.row

    @property
    套路 列号(分身):
        '''返回指定范围第一列的序号, 只读'''
        返回 分身.column

    @property
    套路 原始值(分身):
        '''获取或设置原始值'''
        返回 分身.raw_value

    @原始值.setter
    套路 原始值(分身, 数据):
        分身.raw_value = 数据

    套路 清除内容(分身):
        '''清除一个范围的内容, 但保留格式'''
        返回 分身.clear_contents()

    套路 清除格式(分身):
        '''清除一个范围的格式, 但保留内容'''
        返回 分身.clear_formats()

    套路 清空(分身):
        '''清除一个范围的内容和格式'''
        返回 分身.clear()

    套路 尽头(分身, 方向) -> '〇范围':
        '''
        返回一个表示区域内（包含源范围）尽头的单元格的范围对象.
        相当于按 ctrl + 上/下/左/右箭头键。
        
        格子.〇范围('a1:b2').值 = 1 \n
        格子.〇范围('a1').尽头('向下') \n
        > <范围 [测试.xlsx]Sheet1!$A$2>
        '''
        方向字典 = {
            '向上' : 'up',
            '向下' : 'down',
            '向左' : 'left',
            '向右' : 'right'
        }
        返回 〇范围(impl=分身.impl.end(方向字典.获取(方向, 方向)))

    @property
    套路 公式(分身):
        '''获取或设置给定范围的公式'''
        返回 分身.formula

    @公式.setter
    套路 公式(分身, 值):
        分身.formula = 值
    
    @property
    套路 公式2(分身):
        '''获取或设置给定范围的公式2'''
        返回 分身.formula2

    @公式2.setter
    套路 公式2(分身, 值):
        分身.formula2 = 值

    @property
    套路 数组公式(分身):
        '''获取或设置给定范围的数组公式'''
        返回 分身.formula_array

    @数组公式.setter
    套路 数组公式(分身, 值):
        分身.formula_array = 值

    @property
    套路 字体(分身):
        返回 分身.font
    
    @property
    套路 字符々(分身):
        返回 分身.characters

    @property
    套路 列宽(分身):
        '''获取或设置一个范围的列宽, 0-255, 单位为字符.
        如果范围内的列宽不一致, 则返回 空'''
        返回 分身.column_width

    @列宽.setter
    套路 列宽(分身, 值):
        分身.column_width = 值

    @property
    套路 行高(分身):
        '''获取或设置一个范围的列宽, 0-409.5, 单位为点.
        如果范围内的行高不一致, 则返回 空'''
        返回 分身.row_height

    @行高.setter
    套路 行高(分身, 值):
        分身.row_height = 值

    @property
    套路 宽度(分身):
        '''返回一个范围的宽度, 单位为点, 只读.'''
        返回 分身.width

    @property
    套路 高度(分身):
        '''返回一个范围的高度, 单位为点, 只读.'''
        返回 分身.height

    @property
    套路 左边距离(分身):
        '''返回从 A 列左边缘到范围左边缘的距离, 单位为点, 只读.'''
        返回 分身.left

    @property
    套路 上边距离(分身):
        '''返回从第一行上边缘到范围上边缘的距离, 单位为点, 只读.'''
        返回 分身.top

    @property
    套路 数字格式(分身):
        '''获取或设置范围的数字格式'''
        如果 分身.number_format == 'General':
            分身.number_format = '一般'
        返回 分身.number_format

    @数字格式.setter
    套路 数字格式(分身, 值):
        如果 值 == '一般':
            值 = 'General'
        分身.number_format = 值

    套路 获取地址(分身, 行_绝对=真, 列_绝对=假, 包含表名=假, 外部=假):
        '''以指定格式返回范围的地址'''
        返回 分身.get_address(row_absolute=行_绝对, column_absolute=列_绝对, 
                                include_sheetname=包含表名, external=外部)

    @property
    套路 地址(分身):
        '''返回一个代表范围引用的字符串'''
        返回 分身.address

    @property
    套路 当前区域(分身) -> '〇范围':
        '''返回一个范围对象, 它代表空行空列或工作表边缘所限定的范围.'''
        返回 〇范围(impl=分身.impl.current_region)

    套路 自适应(分身):
        '''自适应范围中所有单元格的宽度和高度.'''
        返回 分身.autofit()

    @property
    套路 颜色(分身):
        '''获取或设置指定范围的背景颜色. 使用颜色元组或颜色常量'''
        返回 分身.color

    @颜色.setter
    套路 颜色(分身, 颜色或rgb):
        分身.color = 颜色或rgb

    @property
    套路 名称(分身):
        '''获取或设置范围的名称'''
        返回 分身.name

    @名称.setter
    套路 名称(分身, 值):
        分身.name = 值

    套路 __call__(分身, *参数) -> '〇范围':
        返回 〇范围(impl=分身.impl(*参数))

    @property
    套路 行々(分身) -> '〇范围行々':
        '''返回一个代表范围中所有行的对象'''
        返回 〇范围行々(分身)

    @property
    套路 列々(分身) -> '〇范围列々':
        '''返回一个代表范围中所有列的对象'''
        返回 〇范围列々(分身)

    @property
    套路 形状(分身):
        '''返回一个表示范围尺寸的元组'''
        返回 分身.shape

    @property
    套路 大小(分身):
        '''返回范围中的元素个数'''
        返回 分身.size

    @property
    套路 值(分身):
        '''
        获取或设置给定范围的值.
        返回对象取决于所使用的转换器.
        '''
        返回 分身.value

    @值.setter
    套路 值(分身, 数据):
        '''获取或设置给定范围的值'''
        分身.value = 数据

    套路 扩展(分身, 模式='表格') -> '〇范围':
        '''根据所提供的模式扩展范围.
        忽略左上方的空单元格 (不同于 <〇范围.尽头()>'''
        模式字典 = {
            '表格' : 'table', 
            '向下' : 'down',
            '向右' : 'right',
        }
        rng = 分身.expand(mode=模式字典.获取(模式, 模式))
        单元1 = xw.Range((rng.row, rng.column))
        单元2 = rng.last_cell
        返回 〇范围(单元1, 单元2)
        #如果 ':' 在 adr:
        #    返回 〇范围(adr.分割(':')[0], adr.分割(':')[1])
        #返回 〇范围(adr)

    套路 __getitem__(分身, key):
        if type(key) is tuple:
            row, col = key

            n = 分身.shape[0]
            if isinstance(row, slice):
                row1, row2, step = row.indices(n)
                if step != 1:
                    raise ValueError("切片步长不支持.")
                row2 -= 1
            elif isinstance(row, int):
                if row < 0:
                    row += n
                if row < 0 or row >= n:
                    raise IndexError("行索引 %s 超出范围 (%s 行)." % (row, n))
                row1 = row2 = row
            else:
                raise TypeError("行索引须为整数或切片, 不能是 %s" % type(row).__name__)

            n = 分身.shape[1]
            if isinstance(col, slice):
                col1, col2, step = col.indices(n)
                if step != 1:
                    raise ValueError("切片步长不支持.")
                col2 -= 1
            elif isinstance(col, int):
                if col < 0:
                    col += n
                if col < 0 or col >= n:
                    raise IndexError("列索引 %s 超出范围 (%s 列)." % (col, n))
                col1 = col2 = col
            else:
                raise TypeError("列索引须为整数或切片, 不能是 %s" % type(col).__name__)

            return 分身.工作表.范围((
                分身.row + row1,
                分身.column + col1,
                max(0, row2 - row1 + 1),
                max(0, col2 - col1 + 1)
            ))

        elif isinstance(key, slice):
            if 分身.shape[0] > 1 and 分身.shape[1] > 1:
                raise IndexError("二维范围不支持一维切片")

            if 分身.shape[0] > 1:
                return 分身[key, :]
            else:
                return 分身[:, key]

        elif isinstance(key, int):
            n = len(分身)
            k = key + n if key < 0 else key
            if k < 0 or k >= n:
                raise IndexError("索引 %s 超出范围 (%s 元素)." % (key, n))
            else:
                return 分身(k + 1)

        else:
            raise TypeError("单元格索引须为整数或切片, 不能是 %s" % type(key).__name__)

    套路 __repr__(分身):
        返回 "<范围 [{1}]{0}!{2}>".格式化(分身.sheet.name, 分身.sheet.book.name, 分身.address)

    套路 插入(分身, 移动=空, 复制来源='格式来自左边或上方'):
        '''工作表中插入一个或一系列单元格'''
        如果 移动 == '右移':
            移动 = 'right'
        或如 移动 == '下移':
            移动 = 'down'
        如果 复制来源 == '格式来自左边或上方':
            复制来源 = 'format_from_left_or_above'
        或如 复制来源 == '格式来自右边或下方':
            复制来源 = 'format_from_right_or_below'
        分身.insert(shift=移动, copy_origin=复制来源)

    套路 删除(分身, 移动=空):
        '''删除一个或一系列单元格'''
        如果 移动 == '左移':
            移动 = 'right'
        或如 移动 == '上移':
            移动 = 'up'
        分身.delete(shift=移动)

    套路 复制(分身, 目的地=空):
        '''将一个范围复制到目标范围或剪贴板'''
        分身.copy(destination=目的地)

    套路 粘贴(分身, 粘贴选项=空, 操作=空, 跳过空白=假, 转置=假):
        '''将剪贴板中的范围粘贴到指定范围'''
        粘贴选项字典 = {
            '全部合并条件格式' : 'all_merging_conditional_formats',
            '全部' : 'all',
            '全部_边界除外' : 'all_except_borders',
            '全部_使用源主题' : 'all_using_source_theme',
            '列宽' : 'column_widths',
            '注释' : 'comments',
            '格式' : 'formats',
            '公式' : 'formulas',
            '公式和数字格式' : 'formulas_and_number_formats',
            '验证' : 'validation',
            '值' : 'values',
            '值和数字格式' : 'values_and_number_formats'
        }
        粘贴选项 = 粘贴选项字典.获取(粘贴选项, 粘贴选项)
        操作字典 = {
            '加' : 'add',
            '减' : 'subtract',
            '乘' : 'multiply',
            '除' : 'divide'
        }
        操作 = 操作字典.获取(操作, 操作)
        分身.paste(paste=粘贴选项, operation=操作, skip_blanks=跳过空白, transpose=转置)

    @property
    套路 超级链接(分身):
        '''返回指定范围 (仅限单个单元格) 的超级链接地址.'''
        返回 分身.hyperlink

    套路 添加超级链接(分身, 地址, 显示文本=空, 屏幕提示=空):
        '''为指定范围 (仅限单个单元格) 添加一个超级链接.'''
        分身.add_hyperlink(地址, text_to_display=显示文本, screen_tip=屏幕提示)

    套路 调整大小(分身, 行数=空, 列数=空) -> '〇范围':
        '''调整指定范围的大小'''
        if 行数 is not None:
            assert 行数 > 0
        else:
            行数 = 分身.shape[0]
        if 列数 is not None:
            assert 列数 > 0
        else:
            列数 = 分身.shape[1]

        return 〇范围(分身(1, 1), 分身(行数, 列数)).选项々(**分身._options)

    套路 偏移(分身, 行偏移=0, 列偏移=0) -> '〇范围':
        '''返回指定范围偏移指定量之后的新范围对象'''
        返回 〇范围(
            分身(
                行偏移 + 1,
                列偏移 + 1
            ),
            分身(
                行偏移 + 分身.shape[0],
                列偏移 + 分身.shape[1]
            )
        ).选项々(**分身._options)
    
    @property
    套路 最后单元格(分身) -> '〇范围':
        '''
        返回指定范围的右下单元格, 只读.
        
        示例
        ---------
        导入 格子
        范围1 = 格子.〇范围('A1:E4')
        范围1.最后单元格.行号, 范围1.最后单元格.列号
        > (4, 5)
        '''
        # 返回 〇范围((分身.last_cell.row, 分身.last_cell.column))
        返回 分身(分身.shape[0], 分身.shape[1]).选项々(**分身._options)

    套路 选中(分身):
        '''选中范围, 仅对活动工作簿有效'''
        分身.select()

    @property
    套路 合并区域(分身) -> '〇范围':
        '''返回一个范围对象, 它代表含有指定单元格的合并范围.
        如果指定单元格不在合并范围中, 则返回指定单元格.'''
        返回 〇范围(impl=分身.impl.merge_area)

    @property
    套路 含合并单元格(分身):
        '''范围是否含有合并单元格'''
        返回 分身.merge_cells

    套路 合并(分身, 分行合并=假):
        '''从指定范围对象创建一个合并单元格'''
        分身.merge(分行合并)

    套路 取消合并(分身):
        '''将一个合并区域拆分为一个个单元格'''
        分身.unmerge()

    @property
    套路 表(分身):
        '''如果范围是一个表对象的一部分, 则返回该表对象, 否则返回空'''
        返回 分身.table

    @property
    套路 自动换行(分身):
        '''
        如果启用了自动换行属性, 则返回真, 否则返回假.
        '''
        返回 分身.wrap_text

    @自动换行.setter
    套路 自动换行(分身, 值):
        分身.wrap_text = 值

    @property
    套路 注释(分身):
        '''返回一个注释对象'''
        返回 分身.note

    套路 复制为图片(分身, 外观="屏幕", 格式="图片"):
        如果 外观 == "屏幕":
            外观 = "screen"
        或如  外观 == "打印机":
            外观 = "printer"
        如果 格式 == "图片":
            格式 = "picture"
        或如 格式 == "位图":
            格式 = "bitmap"
        分身.copy_picture(appearance=外观, format=格式)

    套路 转为png(分身, 路径=空):
        分身.to_png(路径)

    套路 转为pdf(分身, 路径=空, 布局=空, 显示=假, 质量="标准"):
        如果 质量 == "标准":
            质量 = "standard"
        或如 质量 == "最低":
            质量 = "minimum"
        返回 分身.to_pdf(path=路径, layout=布局, show=显示, quality=质量)

_反向注入(〇范围, xw.Range)


类 〇范围行々(xw.RangeRows):
    '''代表一个范围的行集合'''

    @property
    套路 计数(分身):
        '''返回行数'''
        返回 分身.count

    套路 自适应(分身):
        '''最合适的行高'''
        分身.autofit()

    def __getitem__(分身, key):
        if isinstance(key, slice):
            return 〇范围行々(rng=分身.rng[key, :])
        elif isinstance(key, int):
            return 分身.rng[key, :]
        else:
            raise TypeError("索引须为整数或切片, 不能是 %s" % type(key).__name__)

    def __repr__(分身):
        return '{}({})'.format(
            分身.__class__.__name__[1:-1],
            repr(分身.rng)
        )

_反向注入(〇范围行々, xw.RangeRows)


类 〇范围列々(xw.RangeColumns):
    '''代表一个范围的列集合'''

    @property
    套路 计数(分身):
        '''返回列数'''
        返回 分身.count

    套路 自适应(分身):
        '''最合适的列宽'''
        分身.autofit()

    def __getitem__(分身, key):
        if isinstance(key, slice):
            return 〇范围列々(rng=分身.rng[key, :])  # 原库这里用 RangeRows ?
        elif isinstance(key, int):
            return 分身.rng[key, :]
        else:
            raise TypeError("索引须为整数或切片, 不能是 %s" % type(key).__name__)

    def __repr__(分身):
        return '{}({})'.format(
            分身.__class__.__name__[1:-1],
            repr(分身.rng)
        )

_反向注入(〇范围列々, xw.RangeColumns)


类 〇形状(xw.Shape):
    '''形状对象'''
    套路 __init__(分身, *参数, **关键词参数):
        xw.Shape.__init__(分身, *参数, **关键词参数)

    @property
    套路 名称(分身):
        '''获取或设置形状的名称'''
        返回 分身.name

    @名称.setter
    套路 名称(分身, 值):
        分身.name = 值

    @property
    套路 类型(分身):
        '''返回形状的类型'''
        返回 分身.type

    @property
    套路 左边位置(分身):
        '''获取或设置代表形状左边位置的点数'''
        返回 分身.left

    @左边位置.setter
    套路 左边位置(分身, 值):
        分身.left = 值

    @property
    套路 上边位置(分身):
        '''获取或设置代表形状上边位置的点数'''
        返回 分身.top

    @上边位置.setter
    套路 上边位置(分身, 值):
        分身.top = 值

    @property
    套路 宽度(分身):
        '''获取或设置代表形状宽度的点数'''
        返回 分身.widith

    @宽度.setter
    套路 宽度(分身, 值):
        分身.widith = 值

    @property
    套路 高度(分身):
        '''获取或设置代表形状高度的点数'''
        返回 分身.height

    @高度.setter
    套路 高度(分身, 值):
        分身.height = 值

    套路 删除(分身):
        '''删除形状'''
        返回 分身.delete()

    套路 激活(分身):
        '''激活形状'''
        分身.activate()

    @property
    套路 文本(分身):
        '''获取或设置形状的文本'''
        返回 分身.text

    @文本.setter
    套路 文本(分身, 值):
        分身.text = 值

    @property
    套路 字体(分身):
        返回 分身.font
    
    @property
    套路 字符々(分身):
        返回 分身.characters

    @property
    套路 父对象(分身) -> '〇工作表':
        '''返回形状的父对象'''
        返回 〇工作表(impl=分身.impl.parent)

    套路 __repr__(分身):
        返回 "<形状 '{0}' 中的 {1}>".格式化(
            分身.父对象,
            分身.name
        )

_反向注入(〇形状, xw.Shape)


类 〇形状々(xw.main.Shapes):
    '''指定工作表上所有形状对象的集合'''

    _name = '形状々'

    _wrap = 〇形状


类 〇表(xw.main.Table):

    @property
    套路 父对象(分身) -> '〇工作表':
        '''返回表的父对象'''
        返回 〇工作表(impl=分身.impl.parent)

_反向注入(〇表, xw.main.Table)


类 〇表々(xw.main.Tables):

    _wrap = 〇表


类 〇图表(xw.Chart):
    '''图表对象'''
    套路 __init__(分身, 名称或索引=空, impl=空):
        xw.Shape.__init__(分身, name_or_index=名称或索引, impl=impl)

    @property
    套路 名称(分身):
        '''获取或设置图表的名称'''
        返回 分身.name

    @名称.setter
    套路 名称(分身, 值):
        分身.name = 值

    @property
    套路 父对象(分身):
        '''返回形状的父对象'''
        impl = 分身.impl.parent
        if isinstance(impl, xw.xlplatform.Book):
            return 〇工作簿(impl=分身.impl.parent)
        else:
            return 〇工作表(impl=分身.impl.parent)

    @property
    套路 图表类型(分身):
        '''返回或设置图表的类型'''
        从 .常量 导入 _图表类型字典英中
        返回 _图表类型字典英中.获取(分身.chart_type, 分身.chart_type)

    @图表类型.setter
    套路 图表类型(分身, 值):
        从 .常量 导入 _图表类型字典
        分身.chart_type = _图表类型字典.获取(值, 值)

    套路 设置源数据(分身, 源):
        '''设置图表的源数据范围'''
        分身.set_source_data(源)

    @property
    套路 左边位置(分身):
        '''获取或设置代表图表左边位置的点数'''
        返回 分身.left

    @左边位置.setter
    套路 左边位置(分身, 值):
        分身.left = 值

    @property
    套路 上边位置(分身):
        '''获取或设置代表图表上边位置的点数'''
        返回 分身.top

    @上边位置.setter
    套路 上边位置(分身, 值):
        分身.top = 值

    @property
    套路 宽度(分身):
        '''获取或设置代表图表宽度的点数'''
        返回 分身.widith

    @宽度.setter
    套路 宽度(分身, 值):
        分身.widith = 值

    @property
    套路 高度(分身):
        '''获取或设置代表图表高度的点数'''
        返回 分身.height

    @高度.setter
    套路 高度(分身, 值):
        分身.height = 值

    套路 删除(分身):
        '''删除图表'''
        返回 分身.delete()

    套路 转为png(分身, 路径=空):
        分身.to_png(路径)

    套路 转为pdf(分身, 路径=空, 布局=空, 显示=假, 质量="标准"):
        如果 质量 == "标准":
            质量 = "standard"
        或如 质量 == "最低":
            质量 = "minimum"
        返回 分身.to_pdf(path=路径, layout=布局, show=显示, quality=质量)

    套路 __repr__(分身):
        返回 "<图表 '{0}' 中的 {1}>".格式化(
            分身.父对象,
            分身.name
        )

_反向注入(〇图表, xw.Chart)


类 〇图表々(xw.main.Charts):
    '''指定工作表上所有图表对象的集合'''

    _name = '图表々'

    _wrap = 〇图表

    套路 新建(分身, 左边=0, 上边=0, 宽度=355, 高度=211) -> '〇图表':
        '''在指定工作表上新建一个图表'''
        impl = 分身.impl.add(
            左边,
            上边,
            宽度,
            高度
        )

        返回 〇图表(impl=impl)

_反向注入(〇图表々, xw.main.Charts)


类 〇图片(xw.Picture):
    '''图片对象'''
    #套路 __init__(分身, impl=空):
    #    xw.Picture.__init__(分身, impl=impl)

    @property
    套路 父对象(分身) -> '〇工作表':
        '''返回图片的父对象'''
        返回 〇工作表(impl=分身.impl.parent)

    @property
    套路 名称(分身):
        '''获取或设置图片的名称'''
        返回 分身.name

    @名称.setter
    套路 名称(分身, 值):
        分身.name = 值

    @property
    套路 左边位置(分身):
        '''获取或设置代表图片左边位置的点数'''
        返回 分身.left

    @左边位置.setter
    套路 左边位置(分身, 值):
        分身.left = 值

    @property
    套路 上边位置(分身):
        '''获取或设置代表图片上边位置的点数'''
        返回 分身.top

    @上边位置.setter
    套路 上边位置(分身, 值):
        分身.top = 值

    @property
    套路 宽度(分身):
        '''获取或设置代表图片宽度的点数'''
        返回 分身.widith

    @宽度.setter
    套路 宽度(分身, 值):
        分身.widith = 值

    @property
    套路 高度(分身):
        '''获取或设置代表图片高度的点数'''
        返回 分身.height

    @高度.setter
    套路 高度(分身, 值):
        分身.height = 值

    套路 删除(分身):
        '''删除图片'''
        返回 分身.delete()

    套路 __repr__(分身):
        返回 "<图片 '{0}' 中的 {1}>".格式化(
            分身.父对象,
            分身.name
        )

    套路 更新(分身, 图像):
        '''用新图片替换现有图片, 获取现有图片的属性.'''
        返回 分身.update(图像)  # TODO

_反向注入(〇图片, xw.Picture)


类 〇图片々(xw.main.Pictures):
    '''指定工作表上所有图片对象的集合'''

    _name = '图片々'

    _wrap = 〇图片

    @property
    套路 父对象(分身) -> '〇工作表':
        返回 〇工作表(impl=分身.impl.parent)

    套路 新建(分身, 图像, 文件链接=假, 随文档保存=真, 左边=0, 上边=0, 宽度=空, 高度=空, 名称=空, 更新=假) -> '〇图片':
        '''在指定工作表上增加一张图片'''
        返回 分身.add(图像, link_to_file=文件链接, save_with_document=随文档保存, 
                    left=左边, top=上边, width=宽度, height=高度, name=名称, update=更新)

_反向注入(〇图片々, xw.main.Pictures)


类 〇名称々(xw.main.Names):
    '''工作簿中所有名称对象的集合'''

    套路 __call__(分身, 名称或索引) -> '〇名称':
        返回 〇名称(impl=分身.impl(名称或索引))

    @property
    套路 计数(分身):
        '''返回集合中的对象数列'''
        返回 长(分身)

    套路 新建(分身, 名称, 指称) -> '〇名称':
        '''为一系列单元格定义一个新名称'''
        返回 〇名称(impl=分身.impl.add(名称, 指称))

_反向注入(〇名称々, xw.main.Names)


类 〇名称(xw.Name):
    '''名称对象'''
    #套路 __init__(分身, impl=空):
    #    xw.Name.__init__(分身, impl=impl)

    套路 删除(分身):
        '''删除名称'''
        返回 分身.delete()

    @property
    套路 名称(分身):
        '''获取或设置名称对象的名称'''
        返回 分身.name

    @名称.setter
    套路 名称(分身, 值):
        分身.name = 值

    @property
    套路 指称(分身):
        '''返回或设置名称指称的公式, 以等号开头, 采用 "A1" 表示方式'''
        返回 分身.refers_to

    @指称.setter
    套路 指称(分身, 值):
        分身.refers_to = 值

    @property
    套路 指称范围(分身) -> '〇范围':
        '''返回名称对象所指称的范围对象'''
        返回 〇范围(impl=分身.impl.refers_to_range)

    套路 __repr__(分身):
        返回 "<名称 '%s': %s>" % (分身.name, 分身.refers_to)

_反向注入(〇名称, xw.Name)


类 〇宏(xw.main.Macro):
    套路 运行(分身, *参数):
        返回 分身.run(*参数)

_反向注入(〇宏, xw.main.Macro)


类 〇工作簿々(xw.main.Books):
    '''所有工作簿对象的集合'''

    _wrap = 〇工作簿

    @property
    套路 活动工作簿(分身) -> '〇工作簿':
        '''返回活动工作簿'''
        返回 〇工作簿(impl=分身.impl.active)

    套路 新建(分身) -> '〇工作簿':
        '''新建一个工作簿, 新工作簿成为活动工作簿.'''
        返回 〇工作簿(impl=分身.impl.add())

    套路 打开(分身, 全名, 更新链接=空, 只读=空, 格式=空, 密码=空, 写保护密码=空,
             忽略只读建议=空, 来源=空, 分界符=空, 可编辑=空, 
             通知=空, 转换器=空, 添加到最近使用列表=空, 本地=空, 损坏加载=空) -> '〇工作簿':
        全名 = xw.utils.fspath(全名)
        if not os.path.exists(全名):
            raise FileNotFoundError("没有此文件: '%s'" % 全名)
        全名 = os.path.realpath(全名)
        _, name = os.path.split(全名)
        try:
            impl = 分身.impl(name)
            if not os.path.samefile(impl.全名, 全名):
                raise ValueError(
                    "无法打开两个名为 '%s' 的工作簿, 哪怕它们保存在不同位置." % name
                )
        except KeyError:
            impl = 分身.impl.open(全名, update_links=更新链接, read_only=只读, format=格式, 
             password=密码, write_res_password=写保护密码,
             ignore_read_only_recommended=忽略只读建议, origin=来源, delimiter=分界符, 
             editable=可编辑, notify=通知, converter=转换器,
             add_to_mru=添加到最近使用列表, local=本地, corrupt_load=损坏加载)
        返回 〇工作簿(impl=impl)

_反向注入(〇工作簿々, xw.main.Books)


类 〇工作表々(xw.main.Sheets):
    '''所有工作表对象的集合'''

    _wrap = 〇工作表

    @property
    套路 活动工作表(分身) -> '〇工作表':
        '''返回活动工作表'''
        返回 〇工作表(impl=分身.impl.active)

    套路 __call__(分身, 名称或索引) -> '〇工作表':
        if isinstance(名称或索引, xw.Sheet):
            return 名称或索引
        else:
            return 〇工作表(impl=分身.impl(名称或索引))

    套路 新建(分身, 名称=空, 前置于=空, 后置于=空) -> '〇工作表':
        '''新建一个工作表, 新工作表成为活动工作表.'''
        if 名称 is not None:
            if 名称.lower() in (s.名称.lower() for s in 分身):
                raise ValueError("工作簿中已存在名为 '%s' 的工作表" % 名称)
        if 前置于 is not None and not isinstance(前置于, xw.Sheet):
            前置于 = 分身(前置于)
        if 后置于 is not None and not isinstance(后置于, xw.Sheet):
            后置于 = 分身(后置于)
        impl = 分身.impl.add(前置于 and 前置于.impl, 后置于 and 后置于.impl)
        if 名称 is not None:
            impl.name = 名称
        返回 〇工作表(impl=impl)

_反向注入(〇工作表々, xw.main.Sheets)


类 〇活动引擎之应用々(xw.main.ActiveEngineApps):
    _name = '应用々'

类 〇活动应用之工作簿々(〇工作簿々):
    套路 __init__(分身):
        无操作

    # override class name which appears in repr
    _name = '工作簿々'

    @property
    套路 impl(分身):
        返回 应用々.活动应用.books.impl

类 〇活动工作簿之工作表々(〇工作表々):
    套路 __init__(分身):
        无操作

    # override class name which appears in repr
    _name = '工作表々'

    @property
    套路 impl(分身):
        返回 工作簿々.活动工作簿.工作表々.impl

应用々 = 〇活动引擎之应用々()

工作簿々 = 〇活动应用之工作簿々()

工作表々 = 〇活动工作簿之工作表々()


