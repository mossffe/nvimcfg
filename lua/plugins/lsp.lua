return
{
	{ -- Source file linting --
		"neovim/nvim-lspconfig",
		config = function()
			vim.lsp.config("lua_ls", {
				settings = {
					Lua = {
						diagnostics = {
							globals = {
								"vim"
							}
						}
					}
				}
			})
			vim.lsp.config("pylsp", {
				settings = {
					pylsp = {
						plugins = {
							pycodestyle = {
								maxLineLength = 120
							}
						}
					}
				}
			})
			vim.lsp.config("clangd", {
				cmd = {
					"clangd",
					"-header-insertion=never",
					"--compile-commands-dir=build",
					"--background-index"
				}
			})

			vim.lsp.enable("lua_ls")
			vim.lsp.enable("pylsp")
			vim.lsp.enable("clangd")
			vim.lsp.enable("rust_analyzer")
			vim.lsp.enable("ts_ls")

			vim.lsp.log.set_level("off") -- clangd REALLY likes logging the most insignificant stuff
		end
	},
	{
		"mason-org/mason-lspconfig.nvim",
		dependencies = {"mason-org/mason.nvim", "neovim/nvim-lspconfig"},
		opts = {
			ensure_installed = {
				"lua_ls",
				"pylsp",
				"clangd",
				-- "rust_analyzer",
				"ts_ls"
			}
		}
	},
	{
		"mason-org/mason.nvim",
		opts = {}
	},
	{ -- Completion suggestions --
		"saghen/blink.cmp",
		version = "1.*",
		opts = {
			keymap = {
				preset = "none",
				["<C-e>"] = {"show", "hide", "fallback"},
				["<M-g>"] = {"show_documentation", "hide_documentation", "fallback"},
				["<C-f>"] = {"scroll_documentation_up", "scroll_signature_up", "fallback"},
				["<C-b>"] = {"scroll_documentation_down", "scroll_signature_down", "fallback"},
				["<C-n>"] = {"select_next", "fallback"},
				["<C-p>"] = {"select_prev", "fallback"},
				["<C-k>"] = {"show_signature", "hide_signature", "fallback"},
				["<Tab>"] = {"select_and_accept", "snippet_forward", "fallback"},
				["<S-Tab>"] = {"snippet_backward", "fallback"}
			},
			appearance = {
				nerd_font_variant = "mono"
			},
			completion = {
				documentation = {
					auto_show = false
				}
			},
			signature = {
				enabled = true,
				window = {
					show_documentation = false
				}
			},
			cmdline = {
				keymap = {
					preset = "inherit"
				},
				completion = {
					ghost_text = {
						enabled = false
					},
					menu = {
						auto_show = false
					}
				}
			},
			sources = {
				default = { "lsp", "path" } -- "snippets", "buffer"
			},
			fuzzy = {
				implementation = "prefer_rust_with_warning"
			}
		},
		opts_extend = {
			"sources.default"
		},
		config = function(_, opts)
			require("blink.cmp").setup(opts)

			local hl = require("utils.hl")
			hl.set("BlinkCmpMenu", {link="Normal"})
			hl.set("BlinkCmpMenuBorder", {link="Normal"})
			hl.set("BlinkCmpMenuSelection", {link="Visual"})
			hl.set("BlinkCmpLabelDetail", {link="Normal"})
			hl.set("BlinkCmpLabelDeprecated", {link="ErrorMsg"})
			hl.set("BlinkCmpLabelDescription", {link="Normal"})

			hl.set("BlinkCmpDoc", {link="Normal"})
			hl.set("BlinkCmpDocBorder", {link="Normal"})
			hl.set("BlinkCmpDocSeparator", {link="Normal"})

			hl.set("BlinkCmpSignatureHelp", {link="Normal"})
			hl.set("BlinkCmpSignatureHelpBorder", {link="Normal"})
			hl.set("BlinkCmpSignatureHelpActiveParameter", {link="Visual"})
		end
	}
}
