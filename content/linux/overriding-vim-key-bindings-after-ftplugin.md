Title: Overriding Vim key bindings after ftplugin
Date: 2017-06-22 10:45
Author: Thanh
Category: Linux
Tags: vim, terraform
Slug: overriding-vim-key-bindings-after-ftplugin
Status: draft

I recently started using [vim-terraform](https://github.com/hashivim/vim-terraform), it checks the syntax on save and keeps the config neat - great stuff! One problem I had was it remapped '<Space>' to 'za' which folds/unfolds functions.
This was rather annoying as I use <Space> for bringing up the [buffer list](https://github.com/jlanzarotta/bufexplorer).

In order to unmap/remap this, I had to create `~/.vim/after/ftplugin/terraform.vim` with this content:
```
nnoremap <buffer> <Space> :BufExplorerHor<CR>

```
This is because the plugin uses an `after-directory` which is only run after the file type (ftplugin) is detected.
Creating your own `after-directory` will override this.
