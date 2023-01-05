-- Mock functions for sandbox testing

local request = {}

function request:go(method, url, body)
    return nil
end

function request:select_all(body, selector)
    return nil
end

function request:select_one(body, selector)
    return nil
end
