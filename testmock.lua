local mock = require("mock")

function dump(o)
    if type(o) == 'table' then
       local s = '{ '
       for k,v in pairs(o) do
          if type(k) ~= 'number' then k = '"'..k..'"' end
          s = s .. '['..k..'] = ' .. dump(v) .. ','
       end
       return s .. '} '
    else
       return tostring(o)
    end
 end

function main(request)
    data = request:go("GET", "http://quotes.toscrape.com/", nil, true)
    quotes = data:select_all("span.text")
    quote1 = quotes[1]
    return quote1:text()
end

print(main(mock))
