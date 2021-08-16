# Hao4K 每日签到 action [![hao4k](https://github.com/zesming/hao4k_auto_chech_in/actions/workflows/hao4k.yml/badge.svg)](https://github.com/zesming/hao4k_auto_chech_in/actions/workflows/hao4k.yml)

该项目改编自 [cy920820/hao4k-signin-actions](https://github.com/cy920820/hao4k-signin-action)

基于 Github Actions 的 Hao4K 自动签到来增加K币

## 功能

- 每日凌晨 0 点定时开始执行签到（可自定义）
- 使用[BARK](https://github.com/Finb/Bark)通知结果

## 使用方式

- Fork 本仓库
- 配置 hao4k 账户信息（由于是敏感信息，所以将其配置到了仓库 `setting/secrets` 下）
  - Settings -> Secrets -> New repositoty secret
    - Name = HAO4K_USERNAME, Value = 
    
    - Name = HAO4K_PASSWORD, Value = 
    
    - Name = SECRET_BARK_KEY, Value = 
    
  ````
  对应到[.github/workflows/hao4k.yml]line 27, `env` 下的三个 secret
    - HAO4K_USERNAME
    - HAO4K_PASSWORD
    - SECRET_BARK_KEY
  ````

  - 配置到仓库的 `setting/secrets`
- 修改定时任务时间，在 [.github/workflows/hao4k.yml] line 8, 修改 cron 计时表达式（UTC 时间），参考 [schedule](https://docs.github.com/en/actions/reference/events-that-trigger-workflows#scheduled-events)

## 自动同步上游代码

> fork 本项目后，使用下面方法自动同步上游代码

安装 Github App [Pull](https://github.com/apps/pull)， 将 fork 后的项目添加到 Repository access 列表中即可实现自动同步上游代码

