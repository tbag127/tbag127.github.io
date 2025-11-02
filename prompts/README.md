# 攀岩新闻AI聚合提示词使用指南

## 快速开始

### 1. 使用提示词
将 `climbing-news-aggregator.md` 中的内容复制到你的AI工具（如ChatGPT、Claude等）中，即可开始聚合新闻。

### 2. 自动化方案（建议）

#### 方案A：定时任务 + API
```bash
# 每周一早上8点自动运行
crontab -e
0 8 * * 1 /path/to/fetch-climbing-news.sh
```

#### 方案B：GitHub Actions
创建 `.github/workflows/fetch-news.yml`，使用OpenAI/Anthropic API定期获取新闻并更新网站。

### 3. 输出格式转换

AI输出的Markdown可转换为：
- **HTML**：用于网站展示
- **JSON**：用于API接口
- **RSS**：用于订阅推送

## 提示词版本

- `v2.0` (2025-11-02): 优化版，增加优先级分级、质量检查清单
- `v1.0`: 初始版本

## 常见问题

### Q: 如何调整新闻时间范围？
A: 修改提示词中"过去7天内"为你需要的天数（如"过去3天内"、"过去30天内"）

### Q: 如何增加或删除关注的选手？
A: 修改"明星选手动态"部分的选手名单

### Q: AI输出的新闻质量不稳定怎么办？
A: 在提示词末尾增加一句："请严格按照检查清单逐项验证后再输出"

### Q: 如何实现自动化？
A: 参考 `/scripts` 目录下的自动化脚本示例（待创建）

## 技术栈建议

- **AI服务**: OpenAI GPT-4、Anthropic Claude 3.5、智谱GLM-4
- **网络爬虫**: Beautiful Soup (Python) / Cheerio (Node.js)
- **数据存储**: JSON文件 / Supabase / Firebase
- **前端展示**: React + Tailwind CSS / Vue + Element Plus

## 贡献

如有改进建议，请提交Issue或PR。
