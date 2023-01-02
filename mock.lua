-- Mock functions for sandbox testing --

-- Element mocks
local element = {}

function element:text()
    return tostring(12)
end

-- Response mocks
local response = {}

function response:select_all(text)
    return {element, element, element, element}
end

function response:select_one(text)
    return element
end

-- Request mocks
local request = {}

function request:go(method, url, body)
    return response
end
