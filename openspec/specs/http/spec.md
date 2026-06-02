## ADDED Requirements

### Requirement: HTTPRequestComponent makes requests
根据模板 URL 和输入参数发起 HTTP 请求。

#### Scenario: GET request with template URL
- **WHEN** `url_template="https://httpbin.org/get?q={{query}}"`, inputs={"query": "test"}
- **THEN** 返回 HTTP 响应（status + body）
