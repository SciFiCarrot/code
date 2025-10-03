local km = vim.keymap.set
km("n", "<leader>r", "<cmd>w<bar>!python %<cr>", { desc = "Run current Python file" })

-- Debugger keys
km("n", "<F5>", function()
	require("dap").continue()
end, { desc = "Start/continue debug" })
km("n", "<F10>", function()
	require("dap").step_over()
end, { desc = "Step over" })
km("n", "<F11>", function()
	require("dap").step_into()
end, { desc = "Step into" })
km("n", "<leader>b", function()
	require("dap").toggle_breakpoint()
end, { desc = "Toggle breakpoint" })
