#!/bin/bash

# --- 配置参数 ---
SLEEP_SECONDS=5    # 每次重试之间等待的秒数
MAX_RETRIES=10     # 最大重试次数

# --- 脚本逻辑 ---
CURRENT_RETRY=0

echo "Attempting to push to origin/main..."

# 循环直到 git push 成功或达到最大重试次数
while ! git push origin main 2>&1; do # 2>&1 将标准错误重定向到标准输出，以便捕获所有错误信息

    # 检查是否已达到最大重试次数
    if [ $CURRENT_RETRY -ge $MAX_RETRIES ]; then
        echo ""
        echo "=================================================================="
        echo "ERROR: Git push failed after $MAX_RETRIES attempts. Aborting."
        echo "Please check your network connection, Git configuration, or repository status."
        echo "Examples of issues: authentication failure, merge conflicts, incorrect remote URL."
        echo "=================================================================="
        exit 1 # 退出并返回错误状态码
    fi

    CURRENT_RETRY=$((CURRENT_RETRY + 1))
    echo "" # 换行，让输出更清晰
    echo "Git push failed. Retrying in $SLEEP_SECONDS seconds... (Attempt $CURRENT_RETRY / $MAX_RETRIES)"
    sleep $SLEEP_SECONDS
done

echo ""
echo "=================================================="
echo "SUCCESS: Git push successful after $CURRENT_RETRY attempts!"
echo "=================================================="
exit 0 # 成功退出