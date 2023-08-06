# filebeat

#### 介绍
python 项目使用filebeat

#### 示例
    import filebeat
    
    # 加载配置，is_linux=True 使用Linux版的filebeat，is_linux=False 使用Mac版的filebeat
    fb = filebeat.load_config('/Users/lhb/work/gitee/learn_elk/filebeat_yamls/filebeat.yml', is_linux=False)
    
    # 运行
    fb.run()



