# 1 转换模块
## 1.1 Excel转CSV功能（xlsToCsv）
该功能实现了Excel文件格式到CSV文件格式的转换。用户可以选择特定的Excel工作簿，并将其中的数据导出为逗号分隔值（CSV）格式，该格式广泛用于数据导入导出和跨平台数据交换。
## 1.2 CSV重命名功能（renameCsv）
此功能允许用户批量重命名CSV文件。通过设置命名规则，用户能够快速地更改一个或多个CSV文件的文件名，以便更好地组织数据文件或满足特定的命名需求。
## 1.3 MIKE里程数据生成（mkChainCsv）
该功能通过分析特定格式的文本文件，自动提取水文数据并生成适合MIKE模型使用的链式数据文件。具体步骤如下：
- 数据解析：程序读取名为secss.txt的输入文件，该文件包含了断面的坐标和信息。
- 里程数据生成：通过识别输入文件中的断面编号和坐标，将这些数据转换成链式格式，并计算相应的断面里程（Chainage）。
- 自动化处理：用户有选项在每条支流(branch)的开始和结束位置自动添加虚拟断面（标记为'virtual'），这有助于在MIKE模型中定义边界条件。
- CSV文件输出：将处理后的数据输出到名为chainage.csv的CSV文件中，方便用户进一步操作或直接导入到MIKE模型中。
- 可视化查看：生成的CSV文件可以自动在Excel中打开，方便用户进行查看和验证。
此功能强调自动化和易用性，可大幅度提高水文数据处理的效率和准确性，尤其适用于需要进行水文模拟或环境评估的工程师和研究人员。
## 1.4 转换模块宏（Conversion Module)
转换模块宏可能是一个提供自动化执行上述转换任务的宏指令功能。用户通过宏可以一键执行多个转换任务，从而实现批量处理和提高工作效率。它可能包括宏录制、编辑和执行等功能，以适应不同用户的定制化需求。
这里是一键执行执行转换模块的
 Excel转CSV功能（xlsToCsv）和 CSV重命名功能（renameCsv）
# 2 处理模块
## 2.1 根据河流(river)拆分CSV文件（splitChg）
该功能通过chg_split.py脚本实现，其主要步骤如下：
- 读取CSV文件：脚本首先读取位于processed_data目录下名为chainage.csv的CSV文件，该文件包含河流的各个测站信息。
- 验证CSV结构：脚本验证CSV文件的列数是否符合预期，确保数据格式的正确性。
- 根据河流拆分数据：通过河流名称将数据进行分组，每个河流的数据将被拆分为独立的CSV文件。
- 保存拆分后的文件：每组数据被保存在processed_data/chg_files目录下，文件名格式为{river_name}_chg.csv，其中{river_name}为河流的名称。
## 2.2 根据支流(branch)拆分CSV文件（insertChg）
- 该功能由chg_insert.py脚本实现，其工作流程包括：
- 加载测站数据：从CSV文件中加载测站(chainage)数据，将其存储在字典中，以支流名称作为键。
- 处理断面文件：读取断面(section)文件，并根据测站数据插入新行。这些新行包含测站的附加信息，如支流名称、测站编号等。
- 保存处理后的文件：每个断面文件根据支流名称进行拆分，并保存在processed_data/inserted_files目录下，文件名格式为{prefix}_{branch}.csv，其中{prefix}通常是断面文件的前缀，{branch}是支流名称。
## 2.3 清理CSV数据（cleanCsv）
clean_csv.py 脚本的作用是清洗CSV文件中的数据，移除不需要的行。具体步骤如下：
- 读取数据：从指定的输入文件中读取数据，这通常是包含断面信息的CSV文件。
- 清洗规则：确定何时开始处理数据（例如，在遇到特定关键词“断面名称”时）。在达到某一条件（如“点号”出现在新的断面前）时停止处理，这保证了仅处理每个断面的相关数据。
- 保存清洗后数据：将清洗后的数据写入到新的CSV文件中。这个新文件不包含原始数据文件中不符合特定格式要求的数据行。
- 输出文件：清洗后的文件保存在processed_data/inst_cle_files目录下，文件名与输入文件相同。
## 2.4 生成MIKE文本文件（mkMikeTxt）
- mkcc.py 脚本负责将清洗后的CSV数据转换成MIKE软件可以读取的文本文件格式。转换过程包括：
- 读取和解析数据：脚本从CSV文件中读取断面数据，包括坐标值，并对这些数据行进行解析。
- 数据标签分配：为坐标点分配特定的标签，如最左岸、最右岸、最低点等。
- 格式化数据：将数据按照MIKE软件的文本格式要求进行格式化。这包括断面的名称、流向、坐标点、水位参数等信息。
- 写入TXT文件：将格式化后的数据写入到TXT文件中，以供MIKE软件使用。
- 输出文件：生成的TXT文件保存在processed_data/txt_files目录下，文件名通常是基于CSV文件名但以.txt扩展名保存。
## 2.5 处理模块宏 (Processing Module)
转换模块宏可能是一个提供自动化执行上述转换任务的宏指令功能。用户通过宏可以一键执行多个转换任务，从而实现批量处理和提高工作效率。它可能包括宏录制、编辑和执行等功能，以适应不同用户的定制化需求。
这里是一键执行执行处理模块的
根据河流(river)拆分CSV文件（splitChg）,根据河流(river)拆分CSV文件（splitChg）,清理CSV数据（cleanCsv）和 生成MIKE文本文件（mkMikeTxt）
# 3 虚拟断面模块
## 3.1 获取虚拟断面终点（getVirtEnd）
get_virtual_end.py 脚本的功能是从一系列CSV文件中提取虚拟断面终点的数据。具体过程如下：
- 读取数据：脚本逐个读取位于processed_data/chg_files目录下的CSV文件。
- 数据提取：对于每个文件，脚本检索标记为'virtual'（虚拟）的断面，并且其chainage_v值不为0的行，这些被认为是虚拟断面的终点。
- 数据汇总：提取的虚拟断面信息被汇总到一个列表中，包括文件名、虚拟断面类型和值。
- 写入输出文件：所有汇总的虚拟断面数据被写入到all_end_virtuals.csv文件中，保存在processed_data目录下。
- 后处理：利用外部命令sed和sort对输出文件进行清理和排序，去除空格并按第一列排序。
## 3.2 虚拟断面开始（virtStart）
virtual_start.py 脚本的功能是在MIKE软件的文本文件中插入虚拟断面开始的标记。步骤包括：
- 读取文本文件：脚本读取processed_data/txt_files目录下的文本文件。
- 定位并修改：在每个文本文件中，脚本找到第一个断面的结束位置，并复制第一个断面数据作为虚拟断面的内容，将chainage值修改为0。
- 插入虚拟断面：修改后的虚拟断面数据插入到文件的开始位置。
- 保存新文件：处理后的文件保存在processed_data/txt_virtual_start目录下，文件名与原文件相同。
## 3.3 虚拟断面结束（virtEnd）
virtual_end.py 脚本的主要功能是为每个MIKE软件的文本文件添加虚拟断面结束的数据。具体步骤包括：
- 文件读取：脚本遍历txt_virtual_start目录下的文本文件，这些文件已经包含了虚拟断面的开始数据。
- 断面数据提取：对于每个文件，脚本读取内容并识别所有断面，包括虚拟断面的数据。
- 添加虚拟断面数据：将最后一个完整断面的数据复制并附加到文件的末尾，作为虚拟断面的结束部分。
- 文件写入：更新后的文件内容被写入到txt_virtual_end目录下的新文件中。
- 错误处理：如果输入文件不存在，脚本会输出错误信息。
## 3.4 更新虚拟断面终点（virtEndUpdate）
virtual_end_update.py 脚本的作用是更新已有的文本文件中虚拟断面的chainage值。操作步骤如下：
- 映射创建：从all_end_virtuals.csv文件中读取数据，创建一个映射，关联文本文件名和新的chainage值。
- 文件更新：脚本遍历每个文本文件，读取文件内容，并在指定的行更新chainage值。
- 内容定位与替换：在每个文件中，找到倒数第二个分隔符后的第三行，即虚拟断面数据所在的行，然后更新该行的chainage值。
- 保存更改：将修改后的内容写回到txt_virtual_end目录下的相应文件中。
- 异常处理：若文件不存在或格式不正确，脚本将打印错误信息并跳过处理。
## 3.5 合并文本文件（combineTxt）
本函数的功能是将'./processed_data/txt_virtual_end/'目录下的所有文本文件合并到一个名为'combined.txt'的单一文件中，并将该文件放在'./processed_data/'目录下。 具体步骤如下：
- 检查'./processed_data/combined.txt'文件是否已存在，如果存在，就将其删除。
- 创建一个新的'combined.txt'文件，用于写入内容。
- 对'./processed_data/txt_virtual_end/'目录下的所有'.txt'文件进行遍历。对于每一个文件： 打开该文件用于读取内容。 将文件内容写入到'combined.txt'文件中
## 3.6 虚拟断面模块宏 (Virtual Section Module)
转换模块宏可能是一个提供自动化执行上述转换任务的宏指令功能。用户通过宏可以一键执行多个转换任务，从而实现批量处理和提高工作效率。它可能包括宏录制、编辑和执行等功能，以适应不同用户的定制化需求。
这里是一键执行执行虚拟断面模块的 获取虚拟断面终点（getVirtEnd） ,虚拟断面开始（virtStart） ,更新虚拟断面终点（virtEndUpdate） ,更新虚拟断面终点（virtEndUpdate） 和合并文本文件（combineTxt）
# 4 插件系统(plugin) 
## 4.1 主题插件
- 初始化（initialize）：插件启动时，会在应用程序的菜单栏中创建一个名为“Themes”的新菜单项。
- 创建主题菜单（create_theme_menu）：在“Themes”菜单下，为每个可用的主题创建一个菜单项。
- 创建主题动作（create_theme_actions）：为每一个主题定义一个动作（Action），并分配一个快捷键。当选择特定主题时，将触发一个事件来改变应用程序的外观。
    * 苹果混合暗光主题 (Apple Dark Light Hybrid) - 快捷键：Ctrl+1
        * 一种结合了暗色和亮色元素的混合主题，适合喜欢在两种风格间切换的用户。
    * 经典苹果亮色主题 (Classic Apple Light) - 快捷键：Ctrl+2
        * 传统的亮色主题，带有经典的苹果界面色调，适合喜欢传统苹果风格的用户。
    * 优雅暗色主题 (Elegant Dark) - 快捷键：Ctrl+3
        * 一种简洁而优雅的暗色主题，为长时间工作提供了舒缓的视觉体验。
    * 极简绿色主题 (Minimalist Green) - 快捷键：Ctrl+4
        * 以绿色为主调的极简风格主题，清新自然，适合追求简约风格的用户。
    * 现代苹果亮色主题 (Modern Apple Light) - 快捷键：Ctrl+5
        * 现代风格的亮色主题，带有苹果特色的色彩和设计，适合追求现代感的用户。
    * 自然启发主题 (Nature Inspired) - 快捷键：Ctrl+6
        * 由自然景观启发设计的主题，使用自然的色彩和图案，给用户带来宁静的氛围。
    * 复古波主题 (Retro Wave) - 快捷键：Ctrl+7
        * 回归80年代复古风潮的主题，具有鲜艳的色彩和复古的设计感。
    * 柔和蓝色主题 (Soft Blue) - 快捷键：Ctrl+8
        * 以柔和的蓝色调为主的主题，给人以平静和专业的感觉。
    * 科技专业主题 (Tech Professional) - 快捷键：Ctrl+9
        * 适合技术和专业领域的主题，具有现代和高科技的设计元素。
    * 温暖日落主题 (Warm Sunset) - 快捷键：Ctrl+0
        + 模拟日落的温暖色调，为用户创造一个温馨舒适的工作环境。
- 设置主题（set_theme）：加载选定的主题文件并应用其样式表到应用程序窗口，改变应用程序的外观。
- 保存配置（save_config）：将用户选择的主题配置保存到配置文件中，以便在下次启动应用程序时能够加载并应用上次选择的主题。
- 加载设置（load_settings）：在插件加载时，读取配置文件中保存的主题设置，并应用到应用程序。
- 反初始化（deinitialize）：在插件被关闭时，将从菜单栏中移除“Themes”菜单项，清理插件创建的界面元素。
