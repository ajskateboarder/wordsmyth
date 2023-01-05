function main(request)
    data = request:go("GET", "https://google.com", nil, true)
    return request:select_all(data, "a.gb4")
end