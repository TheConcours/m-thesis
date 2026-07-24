#!/usr/bin/env perl

# カレントディレクトリ変更
$do_cd = 1;

# uplatexの呼び出し(後で変わる)
$pdf_mode = 1;
$latex = 'pdflatex -synctex=1 -halt-on-error -file-line-error %O %S';
#$dvipdf = 'dvipdfmx %O -o %D %S';
$max_repeat = 5;

# bibtex系
$bibtex_use=2;
$bibtex = 'upbibtex %O %S';
$biber = 'biber --bblencoding=utf8 -u -U --output_safechars %O %S';

# index
$makeindex = 'upmendex %O -o %D %S -s jpbase';

# ヴューワ
# $dvi_previewer = "open %S";
# $pdf_previewer = "open %S";

# 出力フォルダ指定
$out_dir = ".";
# 中間ファイルを別フォルダに隠しておける
$emulate_aux = 1;
$aux_dir = ".tex_intermediates";

# 中間ファイル登録
$clean_ext="$clean_ext run.xml";

# Set the default file if compiling from another directory
@default_files = ('main.tex');

