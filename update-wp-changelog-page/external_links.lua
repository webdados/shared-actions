-- Pandoc Lua filter: open external links in a new tab.
-- A link is considered internal if its target contains the STORE_DOMAIN
-- environment variable. Relative and fragment links are left unchanged.
-- External http(s) links get target="_blank" and rel="noopener noreferrer".

local store_domain = os.getenv("STORE_DOMAIN") or ""

function Link(el)
    local url = el.target
    if not url:match("^https?://") then return el end
    if store_domain ~= "" and url:match(store_domain:gsub("%.", "%%.")) then return el end
    el.attributes["target"] = "_blank"
    el.attributes["rel"]    = "noopener noreferrer"
    return el
end
