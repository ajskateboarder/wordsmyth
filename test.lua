function main(request)
    data = request:go("GET", "http://quotes.toscrape.com/", nil, true)
    quote = data:select_one("span.text"):text()
    return quote
end