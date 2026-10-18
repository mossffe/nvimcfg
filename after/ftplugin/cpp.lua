vim.treesitter.start()

local hl = require("utils.hl")
hl.set("@constructor", {})
hl.set("@module", {link="Type"})
