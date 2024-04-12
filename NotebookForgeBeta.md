# << NotebookForgeBeta>> 
## NotebookForgeBeta File Tree

```
NotebookForgeBeta/
    app.py
    create_jupyter_notebook.py
    README.md
    docs/
        NotebookForge_icon.jpg
    example/
        example01.ipynb
        example01.md
    script/
        activate-notebook-forge.bat
        activate-notebook-forge.sh

```

## app.py

```python
import streamlit as st
from create_jupyter_notebook import create_jupyter_notebook
import base64

def download_notebook(notebook_file):
    with open(notebook_file, 'rb') as file:
        notebook_data = file.read()
    b64 = base64.b64encode(notebook_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{notebook_file}">ノートブックをダウンロード</a>'
    return href

def main():

    st.markdown('''
    
<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/NotebookForgeBeta/main/docs/NotebookForge_icon.jpg" width="50%">
<br>
<h1 align="center">NotebookForge</h1>
<h3 align="center">～Markdown to Jupyter Notebook Converter～</h3>

</p>

    ''', unsafe_allow_html=True)
    markdown_content = st.text_area('Markdownファイルの内容を貼り付けてください', height=400)
    
    if st.button('変換'):
        if markdown_content.strip():
            with open('temp_markdown.md', 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            
            output_file = 'output_notebook.ipynb'
            create_jupyter_notebook('temp_markdown.md', output_file)
            
            st.success('ノートブックが生成されました。')
            st.markdown(download_notebook(output_file), unsafe_allow_html=True)
        else:
            st.warning('Markdownファイルの内容を入力してください。')

if __name__ == '__main__':
    main()
```

## create_jupyter_notebook.py

```python
import json
import re

def create_jupyter_notebook(markdown_file, output_file):
    with open(markdown_file, 'r', encoding="utf-8") as file:
        markdown_content = file.read()

    cells = []
    chunks = re.split(r'(#+\s.*)', markdown_content)

    for i in range(len(chunks)):
        chunk = chunks[i].strip()
        if chunk:
            if chunk.startswith('#'):
                cells.append({
                    'cell_type': 'markdown',
                    'source': [chunk]
                })
            else:
                code_chunks = re.split(r'```python\n(.*?)```', chunk, flags=re.DOTALL)
                for j in range(len(code_chunks)):
                    if j % 2 == 0 and code_chunks[j].strip():
                        cells.append({
                            'cell_type': 'markdown',
                            'source': code_chunks[j].strip().split('\n')
                        })
                    elif j % 2 == 1:
                        code_lines = code_chunks[j].strip().split('\n')
                        cells.append({
                            'cell_type': 'code',
                            'execution_count': None,
                            'metadata': {},
                            'outputs': [],
                            'source': code_lines
                        })

    notebook = {
        'nbformat': 4,
        'nbformat_minor': 0,
        'metadata': {
            'colab': {
                'provenance': []
            },
            'kernelspec': {
                'name': 'python3',
                'display_name': 'Python 3'
            },
            'language_info': {
                'name': 'python'
            }
        },
        'cells': cells
    }

    with open(output_file, 'w') as file:
        json.dump(notebook, file, indent=2)

if __name__ == '__main__':

    # 使用例
    markdown_file = 'example/example01.md'
    output_file = 'example/example01.ipynb'
    create_jupyter_notebook(markdown_file, output_file)
```

## README.md

```markdown
---
title: NotebookForgeDemo
emoji: 📉
colorFrom: blue
colorTo: pink
sdk: streamlit
sdk_version: 1.33.0
app_file: app.py
pinned: false
license: mit
---

<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/NotebookForgeBeta/main/docs/NotebookForge_icon.jpg" width="100%">
<br>
<h1 align="center">NotebookForge</h1>

</p>


## Introduction
NotebookForgeは、マークダウンファイルをJupyter Notebookに変換するPythonツールです。主な特徴と利点は以下の通りです。

- マークダウンファイル内のPythonコードブロックを適切なセルタイプ（コードセルまたはマークダウンセル）に自動変換
- 通常のテキストはマークダウンセルに変換
- 生成されたNotebookは指定された出力ファイルに保存
- シンプルで使いやすいインターフェース

NotebookForgeを使用することで、マークダウンファイルで書かれたドキュメントやチュートリアルを簡単にJupyter Notebook形式に変換できます。これにより、対話的な実行環境を提供しつつ、マークダウンの読みやすさと書きやすさを維持できます。

>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

## Demo
NotebookForgeの使用例として、Cohere APIのClassifyエンドポイントについての解説をマークダウンで書き、Jupyter Notebookに変換しました。

- [example/example01.md](example/example01.md): 変換元のマークダウンファイル
- [example/example01.ipynb](example/example01.ipynb): 変換後のJupyter Notebookファイル

このようにNotebookForgeを使うことで、APIドキュメントやチュートリアルを対話的なNotebook形式で提供できます。



## Updates

- [2024/04/11] [NotebookForge v1.0.0](https://github.com/Sunwood-ai-labs/NotebookForgeBeta/releases/tag/v1.0.0)
  - Streamlitベースのウェブアプリを実装
    - ユーザーフレンドリーなGUIでマークダウンからノートブックへの変換を実行可能に
    - 生成されたノートブックをダウンロードする機能を追加
  - Hugging Faceでのデモアプリをリリース
    - [NotebookForgeDemo](https://huggingface.co/spaces/MakiAi/NotebookForgeDemo)にてアプリを公開
  - ノートブック生成ロジックの最適化
  - ドキュメントの拡充
  - マークダウン解析時のバグを修正

- [2024/04/10] [NotebookForge v0.2.0](https://github.com/Sunwood-ai-labs/NotebookForgeBeta/releases/tag/v0.2.0) 
  - Cohere APIのClassifyエンドポイントについての解説をサンプルに追加
  - READMEファイルを追加し、プロジェクトの概要とツールの使い方を記載 
  - `example`ディレクトリを新設し、サンプルファイルを整理
  - サンプルコードのインデントを修正し可読性を向上


## Getting Started
### インストール
NotebookForgeを使用するには、Python 3.11以上が必要です。以下のコマンドでNotebookForge用のConda環境を作成し、アクティベートします。

	```bash
	conda create -n notebook-forge python=3.11
	conda activate notebook-forge
	```

### 使用方法
1. コードブロックを含むマークダウンファイルを用意します。（例: `example/example01.md`）

2. 以下のコマンドを実行し、マークダウンファイルをJupyter Notebookに変換します。
   ```bash
   python create_jupyter_notebook.py
   ```

3. 変換後のNotebookファイルが生成されます。（例: `example/example01.ipynb`）

### カスタマイズ
`create_jupyter_notebook.py`スクリプトの以下の部分を変更することで、入出力ファイルのパスをカスタマイズできます。

	```python
	markdown_file = 'example/example01.md'
	output_file = 'example/example01.ipynb'
	create_jupyter_notebook(markdown_file, output_file)
	```

## Contributing
NotebookForgeへの貢献を歓迎します。バグ報告、機能要望、プルリクエストをお待ちしております。

## License
NotebookForgeはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## Acknowledgements

NotebookForgeの開発にあたり、以下のオープンソースプロジェクトを参考にさせていただきました。

- [Jupyter Notebook](https://jupyter.org/)
- [nbformat](https://github.com/jupyter/nbformat)

```

## docs/NotebookForge_icon.jpg

```
 JFIF  H H   ZExif  MM *           J        Q       Q      Q              C 		



	
 C   "            	
    } !1AQa"q2#BR$3br	
%&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz        	
   w !1AQaq"2B	#3Rbr
$4%&'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz   ? ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (8Dr (
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(0ܔESȡF QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE PN*9.crY: sK;5-,\'_4+}KZ֭K$L<TFOR$+)=^m5-o?&ZO<y-擫XZ+$S+)A\ZI=E69e24ꒂ((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((' QMi:׾$~P,l i?U.4'hWx/նɨ 
E חx
K%/5AV,O>IEMʫgX}DͽOL?~u^W@ֿ7 PAu,mU?5S<+'.}OHԠO"$o^okd,Ӎ+|M{;M^^20ŵ7+_z7 ~_|,$rTze렋Y<j_6ɬnsXu?,ֲ8rIsg1 mllߺG@u?৚G&v+,DO;fk` zi3?Ĳ%2=;{miG-xw_&\fOH'QOЊNy_*
&W+.c?u5n3]HOϏ E4FX8.bXLȊ.́1:Ƿxoo=ƫ< DV?S3X߶|G4/ZTd<sǖA_U{NO#/z*(?m}[OodzpHw2Bν?8Z\siv H^|Fkxg6WҢk@p}y߈~~ϿG\KɗF~lp0RY{}
^*P&nͫ믃q]0>s0粻\p=_EkڦOg6s޾dG9OB7/a<Zh?Q]V}"8G_+wk(Ŗ-ԝ F _wgx
Zӵ9RXgWVAC>vf4G=9:O~zV56E_I_R+X87.KsފteXz:_9_-Skgod9eeo?>psھ? %Zo>,uČ067*@>[` ƱkcX _S1 #cNe}&?/ɷ~/?5>$h~1aӵ+KycuaǷsʜ7HKfnQH,*( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (.u׺ͮIq4pƽ^F
je%y1Ū+|QR^xGzW) I^W/*G]d[+ZdmkitrE_[8  sDi:-}4\ּ/VQهAi"A; y8
{RNL)8gꞱ7ֶqiX~$^w/~ m[vK,5|m_:<?Oe߶K77l1ﴅO͌ktڗ׊n|;&'q	{`~J._{\룓~
S<57 LIkٜ|o>5F&OƝ@{KYog( 'j  F-7-`ʼh>TC&3 ~ʫc6RL:nхI.A$07TqטO] Ph|= ʶr]9jz&|otXt"H<ou^ 6iI~0^lNt%G?&m_DS6do.R\{v,51GK"דh++fIwĞ ~5M#Rag$ӷH$1|Fŋi7_ٖ嬐3o-gmNi-;J-݋]xY["
s8_Qϟx:N~mcطS5Ivk>/dе֠G+sbk߀k=Fox^5xBa߹sW1QQʔc
i(\o5Xt7XֵmBbL6:dLK# '¼ s+IuɸyOWK  uc1x]oix&LyB.8I?S29@IŹʩgTn=O5Èěw6^;wŵaym>YI{UM|έwo@toػ2M 
8珪a'ÿ|6ii[KbnnL2Gq6N0g8b2A*9/<dʩ5ek0!/O߈ou@&
HvgP3Nx?| 9?d.ϋ^H򤺍YW8\'=(@<iQ
'%BW_, a]KTh.y__T޾$ӅTs\}, }cr]Cqk4gk,eYO_2#|58Riqȟ'!׀kh:5ƭjImX0yjooq gzVg,~$Gw3 ?]h	ƮsidȲYM3R*u_=:o84{c$2潯Hk_ً7G$z*yJʽ<MKb$$ѿL[_x~4WnV% SownIOq
 |k}'MԾ
 l0~P>:ݭW[[Y#(Yc]s:E'e.Z|ִ/@/>$Q}29[~pV3S2~+| n5-CwEeԴ;5A՚H/k:ŷ?%x6٦?<Leպk&9Gvȧ 9URgN۹c󙛱ץ3 +
[eln<W:fxP>r}0HZNE |qIIY]_? >~˞W5+rmc(Q~nW8*'4u
Pݤ~Sf$?irM	?&@;> ||UpL+Si#RnL~ V~|Fxou)aͻ{e5iY_ZA8{ӛ"ypk A|qQ]z͜8e+[Iat}jQGE1z>,^5oMË́o2<FGL/$ƾ
 c-a_C7@3.AgS8SBgW|)~mKH՛I?]7Q9?`k'%Q@((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((3M2*Eg>(ٮo-U]Oڋ6s2 
 s\1TirH*OHz%|(.Oӵ)!tOI+uk>k1}ZA~c97pqӥpΰM{v;)X4k[ʝY:~"hV:gg(O_7mjvO/!O0+<IVvԿxN[t~=kȫFz4r{/H|/kKUn,t
$`$SK{Rs޾r ggt ^+_XYrWJdrG":h*#5A4nhCM^ڟd|O ^(y-R (uZb/᛭S^!G`o,ML4TcZjnբ__Q I"oW^;ʞ-ϡU&S\8S4|pp񆶖l?xu= "i_xg\a6@E"#uyl
c:8UZm<W KoKşKº{ii[߼҈LrǶb!r;-tT6ջ]Bh|KhtdY.eD<g|: z
2F F;Y7瞻K 75I9YS>pzgGo$"7#{x亗Ly*
²9{Aǖ7Z
R5kQ?Mw-L'zW	Ko$VI2rH#ӽ}~ڷԗZmy&(_Cn' _؏_|[Ojڶ귶yl
~8ۼ͎7k2%xFsSWs sǺ-|/qmBGg mPNNzW_'mxwoٵ֥f澱
 6 1V>=f*D6?kͺ*dJS> _U' |b &_._އjŇݲCHSe  Gq=+klvfUHdo־I5K΋6|+byzW5ڋg]䏴a__g aw2Ą	B  ӓ_MxSg}.5~L8k1<<x%u_Fֱ{nYKIJ85_~ /=l/<5=cQtQ`@K08d^LePrW<nen)gv 1 ץ~זkq[{V} ~%|f
<q3-D2ݴoPvz78R:=f]cZ-CzYYIrcO,w;dÇ%:+R|l$ܖWIi0A$c˶fldI?JOp+?4GWKӧ6f|ߜt5/ w3/-_KwAIrl)L[G^
xMoKw(x7ZŽ6K<f$	fEze4R׫ #L=8}:SJ fc_+[axvJ]{\hyv 52 g؟
ǅu/MQ.?XYVi$
3!9OK
Z_:Uǈ5{ѭۉE43 UB j/^g4}n=R
:+q*r<RW-:/+ҍ׹?
?^|//?ٯǍrMյiQc۸0$.;WCt?<w X}"eIsY$f|$s/Qmc$tɺ1?|N}쑿fIgƍst
{Y.~zD^iR0{zgZ[o2D&To<#Io0LdFHEPCb|W>{qmK
ͩEmN[&Gl\[yTӓ;zg7wl}Va`T>}״{{{#Э|"S".$;INW"A>+I+pz&thQF̚naGecʂpY7|U`0.5N:g-|w{	[ymfuR>'γ',;7Ó[,Z:*+uA~ሗagQI;'B@֕yb[?i{
°u
cOm[ROgK[%Y>WUYeqW׽v?|?ŽI=k}7Bc_G5IщYY!ںc(Jʤ[xs7h tcMNK{$S,0ʘH\r/쥡>GIy-*%!I1 Cskc+KkV֗s}@+g\WGtnuk7M~u5"S{1jX∲s\H^#lWkmh\=v>\|Sg>"ZXDtm7Zi$;_-2ލf<t5o e:?öWWٸBdg
TtfWmq<=SH+ d{_:~1E7~#A#D#9S?kz#&΅y;tG͗ o4Bm6Np@b3p99<7>_Z\[ɸbd #n^W^:Z[	HleXv<*
JrM"}m&%[eQnZsŶ']ր# 
M֓˹=ៀ$q%iey6KR!㏼Ѓ^	.>W[4K7iuvON0kc
R)Y;_N>r;bय़<'gIgAlt{߳)hm%
<pkw~v{ꏀ0Bu`>c/쫃\i)'Uj.g! O8-n;s#3癒>{ k$
˹gv7e!AsYG$t:҂~ i)[|F(В2 +"quq>_~~Ο,nO)"bYm +) MLl[u뚌FA2=$_?x~aߚAn W߳?=FOZ*AG`# st֋CJ+'o|L[];v:b&FVsY٣U$EP0( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ȠuT3M4qҦSu*1oD\C}6=NO*e/# kW ΔmT7&HA9Ǿ+i)_18:#_PY>#TѼ3my۶;Jv#qx? oCU巙ɹp6Q8,HĽ,m1K2>o +-ԗX'6JkS4k.i?$_?jKK1edFk˟b'E#Ч񻟡o-&;Kx$O&Fp@8繯
 /M{G_Pd>.6e;XSp?J⮻:=7Syv9+om#4bō3]K\h9.$3e<@<~"~ui0ϧX?Ij~2طʯGh^*,ڎe}Fc}uՏOAU=->XI?/ o%8)$YW?%~jnu	=-H7r=2ަ?O
_-MldC:).@Y0k鯎8t`Zi\;p4xRj5l|
OlW2ǚ>ݲiif2Gmtv8"#z/şm^@w 37>-j-u-1K`N~&48*cM=ʕIrSxfS\cmEI<W0EU
$P:W
K7ʿ~G
(ZuC*tA_)
m=Ҍv^H儯	??>E4
q?~ BtyM8 E~{k1 F5B>6 /hLv}tWn0پ7
N[+,d[0Q CǈumCW&{{4n/ypݣ<"_u.(wEHc^.9I_G| OG|T{hgiy85ioìpy`*הɟ	|w{ƞ8񖧨=,gI*τfB4E89W4mq'/^H%1e?ӿ_k!e h
-G_9z)oMO}˦K_HHat1>:+ ߴg?ٞmƭ4K.oe&:s?L`t(Z9ܔO5x
ŧvwڦxSGk<Ơc;ט~?/&~ywm>,1$ɜ+a/]CƩ[iZYǧ\a) &0|b;<';/^yd=e>c[`RQV,=Tz#35cώ[/n4n: 2OSU6S<u2zׇwk}h$M7V(ܟ`q~{ `~~!7.WxWvHI0"2/%Nqk쿌~<o.iNPOHa&@U6r9$g4 "8]]|?4
O_	Gduα};&TW<tV,+]o[ѥ?Idştȭ7)h`epW?Z|@0N[dW6\ O޹ ͽۖUi 	p3}}:ԭKP\K|^~z|xg<OI{E\^-bv\9e+߁?߃>h ·g6'BXSc\sm0D{p)Gŏcωw2Ikc85Z%?4ѣC|1{E]L]#si)X֞!ʒrz'qaxo+Ch	>
: ڡ~m*[r?s?b: t{DZhju1.Tw/mx? fσ6S'U] `[5%Ԁ,~Wnѐ2s]SdsCt%Oo9vc}6ڂᡒ9
4o+:go-ޫkU
O>&=,\kmܺƫ}oi tE]͌& (n=SO±ѴC~} ilmTeIx?RO?nO.54-1m@['鏛$~;,ǋ|kgip۬Z590_B6qIo nmSZ>U TWWq K[a;zwUbr>
|9u#@rFZMn?=~ x"P\~
<_-,wiǜcʨp0 &j=3lu(Ϳ7o[!FkzW-k D
W-qK,[Prkq]8s~d~gUs/O|u'5gi5}1Xy c SzT> =x^ׇQkq>ʺ^hLU 2G=><QGUPu-]36\w3d}bp#q&3ppHѣďe}${ǿ&wմ=cOtӭ\ZH6WRTcK 
UpUL>sj~>8-æxZ\n`#˗zWPOc GV3ʡc-ws}kjM9*Sq|9w
/W=C60nmqojeJl ͐3^{E8g}܌_MA;6届Xฌjvc)'`>"->8]Aqx#"Ց_nPT(q̙Uqg>|:&׆᛫ҒVaw5aGjo?jŗ]xJԮbG02Ѯvj~>6o3Ig@:eYwx6P 8g|64_2)Eg(ʝˌօ<h>k<9>>⹟qy?;g`E1j"ZCxǾ$7i,ޱ5Vo
ŭ=DyG|??_I|?5+Y,nI$f'e!|}7;K}Kr-#[^xEYCWic~5OMUgo0*DȯrIm[tƏE煮F%dlgSyZ+|WEM2_!Kh-U.R䘛6 .h^v\@L; j7Vbi9.2$U+ի%k\Ӧ>{>|bVhm}qۏZo..%2Ps I<?Ukw_@d׺A ?γ~ gb<7saJ.<X%"`S+տlkj :]]٬vF -	ֵR}BK=+Nz 0?}K'Fkx5ǃti3^;g7oJN?<q ,,ufw<zaxEq
JQc s޸r(\$etlnlqMz?OʟҾ,q+N.?2SK#Z?şM*5Rv7Uns	owWڿJ b{e/khP~Q_3~іL	um/Ho޵L>*3pG֚֝~<7n?j-=7ͭn KѡsPj|_ηf(xj2ì66}pߊ姆jW⫉4kQk{n1a؊~ |xi>#2yn.p>c~/~!/u#To+) yy6,҂)AQYG#ibct~qt?#o	:65Sq~
 ߳ kK1q+}Qcض6ܺƛcWs'?p>-ѫ\>áYK4l|k_7Req5G:L2=kw|9~6kZ7oZVwVf  j]i
>(P[q9Ǧ~WOsJxɴE~>| --leֺR[>Tsռ 
Q~rU\co*hxz'hKExMhwp*CQXEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPE (I:ĹfaↁXٵ
[OO:5JЇ.4/\ߢ?!q,\M4"w`xo*F"V17&yճ%7g+#W}\/RP<OcqqJ~u
EOx\k_D#W![L/%ŏcM_Z%frہ|\pO?)C䶏=I j	p0Tb} y࠺F8^BG_ <ghߝo5:| |.F?+u@L[mI$PwWugh/C	IsI\< nmG=JgT,ra>oĿ&VZ	W+#( p^/۫ZrX	
-''EzG줼tvɎ}\+F #w㦄~tmb0V ߍv_Z}Smѿ]՟
i?N!v,du2{WqCηqˡZ/?K]
f6/ &Z?haVxcw'$_zNe1s]ϴ4
R	Xxj2q/M6ח_g	@VF$$py89SQhή!9ßI?j g*s-s]@Ҭ;Ut?L >дumz[]oU9+1|!Fy
>o"Ẃ;vkWfb]%qdw׼kRk=O5."[תr	fiC@N	c*3'񷋷J?H|	>-z\3Z]Lĉ$3^h|RUe~4iv:<>˪ʸCwF#" lcX'D3#⥞h,!Ec_5Τ 2599{o^R"c [x]|;)Y'k (Cw
^ɕⴑgJWCx IHt#}u+y yamap:c7I~%O;-]a]gb.[	%.F8K]_MxөuvN 5x#OeyMv
iFIu5|k?fx~\߾m&
7ZmcH9?_t_減Qm~QQͷ4TFeYSxgJll4/	Z-mR1uoC+\6߽f"5ӍF̣T%mEWwM70|K5[wSp⳾ I>$}i?gai`T̖8,C66ў-MBGׇcЫO9]oziBImtD)!Lg4ɮW~O؝o:7xb8-Kb"XE
;ՏA'$wЏD~wL?^y7~4kх#F3K!, j/#ዯL<\Z
tf-k	˪+δg _S7/'8t}&9%,I1LU N[§~Vdo `ػMK[Vu=-t<os3 
 {
;6/j^kQP)nn[w8Ԓ9칪~⦱   ;E1
Ba*aIwv?gǆſ5^Ӽ=^5EcG39⠤tb*^<%⏇ڟO	tO#6jO韷.<U Lػv7(WK<g}o^6cfyd	sK>`:V}z|~7z׈ 5M~/\D+3ge! H,=mZZ<{ZֱԲdDݍ\d5~߲W>%=Oa[n5MF8#'Te]ś81d)Aqh>=>oeP֬Ǔocsm牒(]dX+ ds_h wr5sxw;Rk+~6sӓR潭~Gyw>,|9u֥p_I4BY@ؑ,@#~?|Wh!E?ŻU.B4 mSW/)b<(?:E{#!>e8_҉r9J"Z
~>΋i&]CI[{a_s1ּ
 j> Ӽ;3:%ԞM	y\`I3;z
 <u:֛=ϗ;zLȑʩ+*-`HN_&sZxgG.cvhhc=1\:'yW _>"j f;!T?z
w_~{\5d"Jv]ؓVo&?ï']kZ:gka:[G4Av]2 0ߚ?>
t>+]7IŔq+L,wgg$"8+kR8u_?2~1K}mRE5Ý^GWjF;g4a0rA#W6BZ綏)D$p=+] z߇w=
kP}'Ldk۸sy@1qWꗖƕ17 4xƞIeSm1溛" t?|?5nuT\[Cp0SIny}?c  ,
aS[?|C}[>6sO3`D]:$z]qSQG
Vn?>>>8qSMMék6|v*I6-Am'zbMaٖ:_S9妍EBn6lmuO)GfeFNi!B}͡B_	m=>I5u]UL\?#m-8|)L _Y?WAk_&˃ݪ[?^mA
^Fe֊?.+cq[M0`.c5'!
k[g>x7jQ,ڇ*T{I 4w62XE`C'һOxRך\F>/Э:2^9?A>>-*Ⱦ.$g8??~NGiI/9sx+ͦ3-^CG<]a` 7 ؿIJGk]>Z?%[?Z_C/GۻPäx
fh~":Z|Yզ!Y>ir7ꁿmZ9$cNE}OEny6waZjwfoe%2s4eIzk(>:*=K.T6!Iq5D+Q=tוs3h઩Sp8 穆ޝi8Px^$EP
|
Kvs\͟s̰Q>010ig!Xv ~j+ ?e]AXl/p\K-:T1ӵxOWGDPռ-M1P [G$18kTkoCh#ۯ5IiW^<1$	sA8'oksZ^q5J;7p/x xp@x%w"Xw#`pFz׊yW&YGۃE|%>$:Ɵ[E%4	m9
>T191R|I9Kx=^k~Z68y\,DiXd8=f;Lf~$?#M.Yl/KT}Syx7őyMSkGQ>马hJxA%B>`~ߟ
/W1Њ襎M3IiC|)x1 4䞾oKE;
J|.S2¹_ ֶ'=?kXu"fѕ70G,|0ܸѾ4\^Mm9&
^jі× `pkا.jwG-J+nYv0O_}(U?2ɣd۔xSKc>1'~#HZjĖ?d )g}{ ̲F[($g'kMy>[Nsj鄮7| eO~^3_MP 1KcVT'߂i	5gX|ی9+㙿j<'w^jeń&u+8X@H Ǔ;o ᗋṆ;y)HnYt_?;6hv[BӋyy7h `(xkaCj ~2!_<-{+cSHo-84$'̑F =sfρ<#&[O4(#4,13{rZNK;/.5x9@'`Nӌ9+wPaF
*Ee<q[I< J]3f S'{c8bi^}k uvnA-ep??:i6?{쵽M߉7z1YFK"m>%+RUDb9[kޞexJIw&dRUG*cɅ_;rTMۓA%̒/LIͶK\(ּd2kڋ<=5--58e̱9I!<e=|.-G|Umm$#⹗t~O>N}'INxF{kxw3Iy@SW|>#α!$.Ss޾,ƧG	d37]WRIN3U%Qܮ'NAnڴ$r4>
|1vщ!~ S׭β/"FԵCt `Q=󽬛#-FOi6~7ŭƷV"y}gq]U9}'R>c=^xͭƉ ؼh
D};? 5X,ʳ|3iڏK?[V[T[gB1 evG8Ҽ k905Λgc\2T1%{W+ZbU?>&gi[ZZ\=JyЬݎ3^
ݽ/ m}6}>p_ŭkX&Y|
h81 W"Qr9\zζ*Mp:Jr_:G4v&AZ9C_k^3Iω5KZM˩vGD_C~r7b?i $k(_ƹzВ?( g/g~&:^*ekukg$&fC־] CHc<kM?ݍb~T'Жz*g}hnVV@jmÎk@( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( t  x~mOSȳ`je%wQ5|7
K$Zlb
Pk?4Ʋ\%ǐ Þ1T0ݏRMsfLq4pƽY~5Ջ2%~_뿷pu+˫?Va|C Ҭn,U-ˊ󿷪տ_~j߶ׅ9ǩ\Z>_oc\ry<q^
զZt[HeڤL峁DG
0m.NieE|xN/
X.$67Pڵ˴91\Eni8cq5Cz~??OV6֡kb}A[H~3f<Ŀ?oսkɦ'vpGR{⾶i>!ڒ_4h/pbg
fKrM֨v $RuJS9bi%5/kXj*3lm9/j]G \_hП
fN CazF)!#&5 3_1MzI-|0Ŵs{F/ZgMtU]xS'7E$?`3I⧄|dƱ
gh_c3->^;V}V_=דkQDe8(zuzMCq{Z;ԘM~VJKT"]8qUoI?=.f70n?ڣ^Ӿ+x*PolOAsn0YfӨ~5UޛxgiaV:-Ӑ#Y"u} 1<=i>+}QJv-H 󮊁zڱc7F/O?)9i  n~׍)]2s:x]4Wwprَ'w_|.~$~>=Wv+9Y@>_ >O_ 'A]ZA|aA-ͅ<ɵG+ H}X=2J5fniFŹz_ >!IὒŭM}W;y Zß]M7>2/sMi$
G
#wMcw85 u?$LOtOj7eQaےA$FkbP;O}Wآ	#$v,W*7HJ89ZjQ.>V*4Ԫs>.?Dv}*YgEzeyccee8{ @ևK f?GBH<Sw6s<q|]RH$`}/Vi"kk{}FK.=*G漛igo<*weh6܉$S=wSxh6VRH̱A9g2|+N}7Dtg^,uoJK^C1g Dq3Nv3aWK/᰻BQ6OWAUu3|3D,Ƶ
+QԢIQH<qZ1YF?] !~ 5Oº>]g;{pĨqـ;^W !c/[iUm'O]S^jy>*'kJm7:֦kdd2m\A n+?j	oP_| [ǷWjphoDm*aXsIG_C.^Öߧ{Í)m!;~!ވ^6}K:@4Xb,'=+
/)ߌmM'>x~(ug{	5utjHfI3#.WƏxƟ-m43i𽍾.nsRq`tfӍ8wqʏ,I-=# ࢟-_|5mE9j:ACm>a3U/C<Mrh%mq,Zeh3
w +~75g[oxVִdּEq;ysYHA]1#W?~	ִg#]}&s CyHĨ$_*Y-/^4o'V7C 
+GG,6-\4\9?tZ R_x_ ok=. 6P5DDb#c!9a&2p{ic~xcݑJp	٢Y~Uc<Щ=NoHwOӵ~ɋkcgA㹣֭tgkt4lYycԞ|L^5Է	Wk`G7,IXEs=zя,cOi7ݟ$x:Mmsi6!
m1p9_p .9|L mk2j^
P[;V5&0א?<GOxfK{T<^|/~|hJZmߺEɣ w9=ɮz֔VD|+	Z/5&ė:C5Xxbmn f?
x+xZ.xb\
v/nB&!" _377k
KKǆ,|DԮgnf4au0%X@sßYxcVg~[Gи
RLcEVWB+Όv
gmD䚊ў>7yIΦO}#C~=;unVUG]2=T~biR/㎱?}p=,3@wݸgkgM?h/|]~*Zȳxu]NOsDyݰf{ɔj-~xTfqh+$n4[cS#F)V_ZJ?>0XzÏjhR. I;d[9ƽl>,jjW瀵Hcm w3;6ܒq~Y4;Mk4O˝B%8>ֱwz+i}Ik菄mRp0GɢJ
(am z=Ay}~ws>MHRYPnaH8)>?OI}՝mv%ޣ`EU:tْdtzSŴt3"޽mmf6e\^W=|!Ubrx~ =0WKd9l[᭼?	 gkDwږqjżD1~b1чSJՑ%Of!|vf(|8:w'>4MzR 
~~ӟg
7z=zoxo]I}0XZI6)9 sƿ|?V KsMx/71\kJ ʯBkM HUuyi U?m'-daC/͒͌Sǽ~zH |3:Y`2Ė̘M$vW
C|I6:~=oG[FGpF$ ?X  eMN7Qag![{LP#JWᝍůlhƢ/GOh[ {'?̒wK;+;g9 .
JMkŞtڌ-ollV^E$*|zoW?xUM4TFkq`TsO i!ӛIm7^,:@ѐ]_@1v1ڪĳQ	υS
'OM؞5<4v`9?{"Ծx{?h!𾁥wGrzm@l
 _jԨ驧Np۾| jO9YYUԶy-#ީ uP; cW j߉_ &ܞ<4=?70okS&WdlİVI9,|	Qv6Yk] Iҩ Hdzqǖ\  mA8r䭵P}֛7:ŜkB:I~ @[OiggZO
[!FMm2=jK8uK;c9%!Kk~
h]R6QYd@~p_wZXTI=R"֨o~ٿ	/<.
>7VݩKGހi#dI9é?*~#xVk~V7>dIt	9x¯ºƍ.9.mVm̷yOpڬk u YO>zf^7c-ѹeyϭoJg=Yaw=oxFo.|7=ܰo"hG?0<{n}p;ׇ~j 4{I.2i@a[~>0s}c^ֵK}@5KXXc`),@9R9k_U'$ƄCM2XWʒF2c7Jؗ8G}8>gr'e:WEBS 6hԤrU K\6BɦZ?5xgP|bZhNlÙJl
x#4}B^
,VVIWegWlsZѭ{[#>]23^hPj:Wiz'}F.Y8c9_xBR!x^Xe1jarn[7ks;yZ9i GmMg2 #9Mv­9Fq΍DGio%t{mAʲC8T7 gKD$oFTB\r*I+'N3_|:ujyumt|ivϗ7 WH~^]asj3+̖vV>g'tɻ?~!7h6$Y})<egWHU;uҼP>*ʆUAO ;M"
]ɵO&?qE&quh+/..|Ik[kyseQp+X_|Qhڦe9̑FJq_n|"+w
o bW~ܞWLZ}Ɋ :E(#,=k˖GiWw0rF#t*վ |?+՗@8nlep_&JMԋf0zcmyb,j.kMMHuex|?M㯋"է8dԥbp袽7L~kKEoiO y&*b6W]v؏M]eZܖG_uorBq~yFuKk(nq=
x n߅&H׊5188yJyG ɕQ5hn=uO Zb,"@u`
)GHBdϠ|/o/xŭkwIv.2.Ȫ^#𿈾ʟ}OC=ƒ7N;N9aGqFy OzL_F.B,BKVg<^{s'F"߶ /dR^1ds<p|#sޭ,ֲo,6@L܏ƽO~3^_A lͮr|XZդ܊74gaicJk{ q<-9X%@78 XFy?eQ*<юq	tIm8|!EdF9+~y'k]f,4RXǻڠRz]׊tKxO3ci);Ru+y前pjmKu-#GE\KO;62j%	"@3ڪÔ鿳֡~ mo58Ͷ\a]{{f/N -׆oB

χəeBȐ\7|8H}7XIx63i((jL察-c6uխ0v60MgunBII>40(<}kСKMLc `۷*G2(Gc^7Znm}oi!.ᾅ.Jk?j
ŁdV%yN?2Mo|
|kPn,h/9ʘdȞh#n1TTʤ9Z;U84gݩi^/3MK yO1^Oڿ?q01Q
r~8~ԤNm,˸Y2rFvj'7CE>h֩x-
RKWyets7rfE$oah]JQV"$>?f
|Y|A}k"-㵳DI!čskľx26ڀcE?ѡu/=xbmJuQ-Dq分029%ZԴi|U@
zr|њ&b'*=+hE.obT~Ş 4'z=t;DBHlpy\<.
RöӣEi# }g?Q_cxছopA$^
ѕ*] 둏ƼǆѾWSx\jE^c9W4kWxc^ #?5c^ڈp\)X'>G}m rUno^ǐq]Ɓþ"'͢?Ťj)dv'rT,sO #rk,r]fe<zW| >,xi-WXu{4Yd
u#p dN}6M7~
YȚĊ~kɇ?yK~˾. 
V<i$]R3n+VVF4ާ9;4cz,jmY8N'?
 ?!j3iivk;ϧ? +<!m麓Dh,2.9~矵';OJ$%|YC3y5r˒7nn4O"xdYd֐9ߵoC]sOE YH?bW|I 	i5/VxGĈ̵GN<yO	KW |"`\r8Û" ?ʾcE/ilrJ:R/c+rG V(( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( +ƿoHoٯ^U8f Ze>r^^#8rY rb	ٝ89(ׄt~3'vԵ-R^;f=*;df'>|>x#Ff"invHF*"~\WF 
|
t0FۮKYO$-EA*NC>+>躷#8 EIDp78|?,}Ϭc)
<?MZ;iK՘$}z5/^0]6ݥmR^YUK:kR??o x>Y:Oj!;T<+;|Mukxŗ`gAH}]\ \WM'o/M8s/CͿDdۗw4oEܾݿ}yiOo ;6G9|.wu,uuw/K{ZMqk>%nb
*D >Ki<
5&mNζѴK;/4U`pInWQ
uJo菬~ZgkhڂǣȗFْ;؀Ipx7"ci/?t{m.t4*#q$sWk |k7-k9խ[hM_h]9|@ql3q s7#h^cGʙ318SxʴȷlrvSjc 6 w|ehZz6[k"Dc%ח,}z\7?kcλkWG$5\ϪA 'qvʈ_%W5/+6iVFZ1[>nU _3Tkx(5~qJ-NS
q.k' ǉ]࿇z<4JcUEA+IVgRnԜC;Z9<^k:z^Ky=1Aڪ:?RZ׼w,h~כSȈD^.B`=Ek:^cW9ЙK ,ġ>ZFws*ZT읝_

]?V񭏅tۏ5Ɵ <2P,|.F
1]ySC/?v:]i(603Fw s*Χ|~͟ 1QԼW%U̾P	&98 \f =x|%#YxItXØ|nFrEe(IbZ&{3W~QZ^.5#]*is)'sNx:o	|W,_O	tMN<3z~տ׏<3GúWXxH!0[yV&eWy`f;Tnܣ9 ~6k7 >;T YKFH+r>ViRQψ8i~/Z^^wĝb ~</{(nXܟ(s
 KpÎ3Sk:}o(5XN|g8T!4b	-H4f&-wkԴڍ屽OHw>v|Q-Tj_GNF	idUKc%G3INGrN1m/~ Xi:oÿ6'4M6o$ZV$n'-r~*h럅^t'k .oeg6n-0[~#]Ι}Tx`^må1Zi~k%YK/ׄ[[+˸H;F2Qq_Uʹ-giպC󍭈FO+/?g)gYhj ťz̗|%rI,&ey}= pxzgկtI=+5ړOh?qbֹxñizMIqwk{lƞJ,FXحi'U\V  $dKkmRUĤ*8w7
ʫMby/
 Q ࢿ~|hg|Ϗ<a5z#uKD)y1(Y C>%Z|S? gOXծaOvk|W1>! Fn;N޹R*1JU6Lhv7wka#c .v9j|+/[Mfm16nvG6gcKW:u>m?f[.W
297e:/ ,{ړ<s}Y4u)nb) m6	&fu[NR]^#MW឵?un,ZͩiHmSˊJBZBa^z ?|K iaeiw$:jNz" dda 6|}~񷊾%xCԢ|z%p8'5:<g oVv9|J4㴒Ͷ;f3KH
3)t]zӣ)=NwQϥzDpcF Hon%1sֺ~;tυ5W2\\^xZx# v96V8?
 ѼGM6^K~Ic4yQ8rNrZF$k؆'xNI\5?˹ntMп<QkTp_XiwOo@	8' 	Bs0ǽ~u:bc͎OW^: |T}KX1}qF6%$*$\  #Hb6I'%}_%
{cTP)<9
(vo WS|85OGHi(񧉾3E样>!qs7JGl4↗yqP]B_HE%r>lsָqWїM6C 
q45X,#!#)";Òn8Q_A~?gLXXguIuIPf*(+~E
~Ϟ./~\ű/>˦,E*6rIZ~~ >1:_
7q&w>mRPs	q(A$T֏/5e[҉d~mXRs7^SOğ᾽K'EKBQ1״2L1LpW˶?l#֬|]x.mVF_cu)[#݅??__>-|D.EfM8$:ضo(1
#q]nQJ(1P)ozlX<-[~k?&ߋ4Z<H`~"۟<9mI.]R bqi.<&r߽mGP@$V'm[Ѽ?q\[|3хӉF}j30GrX?hئ콡Dw|5=բVk[6ʠEpŹ+.i9Fiow]u- >$i
,g])f3Fw?U /'⇈?
𖉩Vk?Zq}Yq4ͳxuo~ϷV5]㭫ib=op_OH.?&웡 xv*'丙'38H?(rMtF4$sRk}3~ .inI-S0"[#$r*B EWQ|f[ $5`{%6	<Uk.k>4,deRYH`鞵8kVO{
V]CU]z*ϖt+sE)YjmZ>H?{Ğ.]L++N7+m2m;Ko+/ÿ
-JErjHUpqs^Κޣ %KwJ]8Td.yo_	&Kw^A;yǒs}3H̤]۴dRtqτV]27_L|o~MI.<M/X4{ ӬXO, X^2[~.e?
Y|k[SSkxU#y7SEppc T~
H#y$6m8l08 *h)Y5g';~~^5.?xwٗMD 	+tow	>iz_A|\IH?C#ҹj洷h|*1w~+ GՖH,cE$~*Zc \0w	97
B6:.^q֚rO,h@-$'OS<gwVwvw$օHLqƇ3Eu?t*@T,ooǳ3s$bEys[ԙY L+rB٥HJng?}OV;)s1<<HCͺck j7>7t_jZlڔliV$$  8 )=z-{4Hƺx)-<1i3m;0&繸ɚu&Hd ,F:q\SV]3g >C+W)5xHy7&ޛ$s?J4۽ZiϚM)x?a[k=I[_4pW$#G%rE}KdA2I,/{!dS09hxzq-b%N_A|Uk~q8-ש-(^#LgE_Uei.<G&%Mr{W̿<!gxNY>o6miiU	9Vyʇ
x"[c.-|9{j'<MxA[8[Mc 0x&&>Co#ƾ J?%2,ur}j~ѾuO-mGmDj3.>c#$s@%/o 2IqcI`G|K_wg\xT߶ݮȝCK`99C
>Ay=h  գeivQeL2K<QP[V	~q=),w\w<?{uGsirn"E*ܓV|Sqcm-ǓpxMyqګђ,D.0~ƥqGVH$br%>V]7Zck3و%@ 8<fm_MpP|s"Xt}`svK/k*?c9J\;şka잃rFNiM9m<MqGm{Ҿ-}+74;IvwM1{}{~Odq0Xqs¼\׈?]dZH';yopHWO9{J17cxZw^u]2i%;mܤڙ[+f+aj/n<5
R=X~M&}Fz'L6'+gO?d7_*^)d o
 Hh7
0nҮ)8G
iEmXnw?_}~?A^3'KU۝s~5zMZCW}ղ|,Rrx{׵~_t#w^kPvZe/5	"C98B9ԧ.Wug!8
|4ߣo7 ~xkY#Zվ:=#G5}64 m;L$8$eRmٖ9PccSNldsGmA"wRܽ	%HH7ekv*hvHoiZ,, 2qǩ|k4(n!{MC1ο~͢Z躃yp ĮB7dub9%xayW+o*<Y(PWQkP{0Ig#s%BH$XKE6b
U FE| ٯWgMƙ"ϥ
F)m0	7p2j#vJ/KYj[ 5FJj(«h l=1<-7|sH51[Z8V!qe$ *>8|U5ǯ[|?_-Y`Eƙz ,c;F[$>:45  WQ&^3o[N9?Μe=Y>2ŉ_ap:/xVԴ[,EepHm2/^9K'V\OO>$<1uu9 <ֆg_Vr ]+I4K5$r͏!'859П}GSGgGkKpi_gUuDUWH"Fe*ãzc?_|/!MM`,`#y,mPXJm/McO67q  5&;/o ܓY/W!(~/|&Ǆt8|Q/Ipۧ6-3 G-a9cLzdVMW$]5bW@]ɒ1^Y~_١V2\י)F8QY
e>4r<?FL!۷e7`u~ާkjnKvZ0a(x8vKV|Pך9c iL]dg=6fG?I~<Ҵ -Ǚو.A~">%Ds_Z>s3<SA#
8ܩSOwxNJ٥U,
Fs|UM7\\ٚWvԆ<wkIu/ѥ7TӒ<3*nCv k/iב_%ԗk=j d&A܈v.G$2E'|Dk{Ff{k/v}Sr	a26yE
7ߌImkᮍYJ͡LrFNHdi^6}6>&x/uw֡\%'@\֡$v\~51~vu~>&?$lE.iubf(U܀>~^?/xa;_\a'In2HDğ,~>[ǩo_eWO0e
 h^uzם~ 'h7^/]]rlpoqV9ஙjBSQh?g?uմGMoiEŻF7fI=WU)Y }IA~ |0ׇfHnA
ʖW~JFRB8~T1rV:guh}գ2NUWk@OD$K-WE>F__MRecmK7LF\1ד޳~~{}-|9-==:-P8TC(?mNzuk6N
uV3ng*rMO/Iƺd#mGZIv:1kAW21\s_|	mclIb&]4nS g
cQ^9Zºyz>(j fOj^r[\\HqH|uk|T,ͤhc5,WF8$WISXi~Ͼxx_hsM(_ >M'ōu
F`ߩ sO<y+I^٠Y zOao⫈x[]>ys8@@;?lG'zz֛2Ư:[XUE=SMkA/+ !|#m[s4}Ūimx5j
|EmWF,aʄXpABz?0Լ/f}izW1m;Fб,A?a,zG$V_Cz9VO |xmYv/D7*44AA?!m')5o6\Bc2²pkXY-QT$~Q___<QgxfDt;mUH{WFW3[IMER(( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( + osu.0Xnd17{Eyg핦6?xUUUK| ͌քٝM+E77^l8n-uEc)}3zo ~PҼ9kjv}ܶrd%Lhr9q]?xMo4!LQ&#%*nM8W=|&(xGoeqp$XCwh/7'q
4{HB7SZ͞i _Xj:?
>Arh!FV'Kſ _
X|>ԣkh1h~ݍ<q\ ૟ |.a6k0X:f-<oCn8<_,O ~xwE;UVʊ$VjCHT%ve*\>u{[K?0ctٌ#ۮEm[: izVO5+Ȃ$Est2zWv>0WW0k6m?yF͗˒e@CfKſN;ωKx^75YnWUon(*V!#WG*iMiN~-s|gҵK5^P?9+&w#.e^{ /+xB
Te7^ᑭopw	G_~^"gc:&E Av>_Gt=&44T[4.m%pqҦ1&Sij__ ~6>*.?;kRxKE:+$cy"\)=O|M<Pz>Y^o&x-XP.q78\9\zv$|o4vWWUCeIT^HZ[Lc\Zgy=GxV_|2UVXCRIߞ.G_Ə;xkxf]R[(m平&D¸? xnNuŠ%n5Yi\FD7'*23^h/ ~ǀt`Yh׭lZo٤rّ
k
C~+|8៌^1#|<~<007%TA;sDT[\j+|
_cxOޒ$g0Hq]Vc:_Z\\޼ȒA8Gx /n?kqVkd.Wj#ngjn8__}{Śv'\^[ѥhPsojs0Gt*՚}u/vf}\o.Fc*u\>gҰ%A -]ǌqk[Ix;r׎ dxǏ@~#k:tZ=q$i#D/L'½OPk;JPtCRR70F=o$:ѹ?gxO NoĲ{-3^MHcu4 hD>#j[j75Ah4`svEml~]_hgZ:@kˇ}-scR[mP&)w#(sƵ7)+CJrMGoڇWG_߃~5.~^Yy[ƻP8/
C]k]zgݰbPe W5:
 >kVuwm=,iZFy@X
ো$*z=Ɵkf/^Rڪn{9-Oq.Dgm *~xVԼ[}~4E{;@ܥggCt@z׷x3Mwh>t^˃/dd)m͇wۧ/Ɵ>
q>#[xScn01!/ h\joVvOj `|=pܕ.
95#osȭj̱毆|A)s;#89T7G3ݬi(Y= !hw 
~ x0^j>]R8կe1ʝV <Qygsݞzw{f!╙| ;H^Z*ȿk+C_$ΘT!U݌r=Eq~g5o)wz?T{E!r<9W
Nt|'}INvXQevncОxGK|cߌ^ Oh "[Rͯ%lA72]yki vNUG]kZ~_\[-p.cr܌>o_cK𿋾3|=ҼMs?/#_jS$A"1KF@!/
^$_jm滼2I3\Y♺ 85߱C4Eւ|?:R&E.WfĈ;szM Ve^Gs
>$D$ěch3ZiaGoVRYX=N7*{+oYxtE{1C:,6,1Ӧ8i	OScup74V/,lbD", Ev9 ~_u
7LMZKI;> q[5O=W$uF|n dkgw[Y&
*p4t q7Dhc4ke֧ynMR]7nCG8I%_akku,v~8#y6mU,xUx=jCo+݌dI78xGG3(+Z?; eO&4x7ZV[9VH\\!oF0xzqg c^cRyn^ϸnn$drWE  
I5V|ax cY$"iP>2c'_?	|*-f>$I	4ъ[͆[wvn0BnKF}1NUCoG֏G`D@HbݎH5Ovmσı6&FxF&Awz瞕UkWޫ
뛙"n6
Pw(Lg=sO<[ox7_}4RI-OyzUFY$FQ CQ5͕ƛ$O[M"r30qԊ>k 	>6cb0eT#]3ÎWguhtKsM{UCf|u z{
YNCq'V"nka_pRuRS~C0ZO kރ*iu|_]nqɸ$䑎3^+o|76x??~8xfODaG*:ʹ遹2 |//c|fzƳ~̷yv;A>Akd5!Y\,D`veߌ'ýcs?c?ڴ,Uνp&߰9Ev!AG Z2վ࿂2
7N]>u]Z8ЩH0
~h-Meya?'S|jwֺr2ǲfs5f@v/ަ<oȉJ2~ K2% -؂G E=T
 Q~%x8n>#^Z)'~pZd	WLfMKr899'ߞ+95+߶	5.{~|DM55FWb&'Z =jmPفv@J[$y$
_[:77o<#Zʧ1`~GZi
q;B}沢Ic·wPV/;VR+ѭ~&bn"<jffXaWb1\kYTE콗kW~#2ZnRΦ*uz,:f 9d+Rɸ]yy챌ҼռQDfι`n-
hR=}{T۴5J]cQ:j>$J	TGnUs֍ n[ӁcЧԉonڵSTP?Ү? ^9~$.~ggG޲-c.mꁿ}nĖe=pYsmy9<qKTٍ^_/K'+\+}T^v30 I 3Xu?TbN'xV@?
\׬[@IFfZڕPOjR6{ 5)zPYrL
2>aVM[@oy_$
L<8ExOo{B6Q]	%(bSKGGpplyǩqdסJq{tOڷZ7
7ī(?]&ԝ-G_
6v6BZο4q\s	j7읤XWVrIצIJ짛c5]<ʸ;wpGVWu{.BK;w
m2Hq7=o
5oǪh1|?y8mmrN:x+3!oLU]YaR5ecJbIp(÷G6K9tmsºVp
[`)yyg_xPڽ߅)`q{o"Tw!1yk<e6r*oc'$$)CҞ"П]z6a#in|cқfU2xJ;;}׭m,R\B0>UzVaTϵE]7Q4_CŻEyqcXDrGr.v38W5;u	h$ji 3e8*3wC3U_Q<-xr| o `ceeUdr0rrI=ɮ'ÿ>5a;3ǹ^q+f[4~h*Eϲ<'L-coa
:W4RKa)݈^rvp8䁞FTe4f5%QGO>Q>	}jsmrH"O"a{
/75_xM40!ǮYèP@87H0=+/?fxsM'cYf\(["7<uvV4?۴xg<Kd:0]Gdz?z>*j$ts>i&ڭٮQI2*o6_>=Zg'cx/ADdqD2ݨ"1eOxˮ<7vc\OX~j̖VQGj!
<ڪ"P\e.Q*.m$H2W<V?]mZ_l~}̌V#	I?M+h_\Kj[6g%frny+Ծx^_ͥZ,܈zi/:9x^k~IROkXv7
-q 'UK+"UJrJLK y7WQ v
q<W)o{wR%L@ʯ=+׼eM.O	Kg]wH$
Zr_'漺έqg|.49e[
EI^23.AAC 3Y֨kQvgeSN/|)֮[B،uexy? :{16#i,;b+' 0_x'KEV':,d줯5:H{CZnu
8yB-<C3R;~㷨1Y	lW4㹿o^(a?j6~#՛^Jъ_j27.(P\4mi߄~tDm2K g Ìk׾|.7 chZVL-n].%vnV\rko	 hxP/FgO Ei3khR_^ <#hpb(mO%A*
r9į*D連+I3Gwa,w
2s;V[~t?x.cvv$-zn~
4kRɫ
^-Ν"m-DA3y

|i%vSOVLӬ57ïُMi]ׇ_sI\|;s֭xgWO=x|i<V\nekd? &3T]~~X_/JqYwcw9>jn1_uNӚ>;#IYZT-aA8Ϗ#jƗoYZK{H5WN?匘ccRWo|@|׾5
%V/	K$cҤԼ[c)~ڷP
:%d4!*͒I=85>$/gxwƞU𶴗k6>Ɩ,@Xjg5W
ծnӮ4~npx!F9ϭ8$4r}~xZ .>٠K/WR; iI 9
~2~5oj~wM{DbQIlfΤjk8\˵-]:Zݭe?s?t>d2ߚڝ>^^֠:!/0!'J9L y WxW:^ui4v7ַe_?QX`laT~"tkVz^gs($662grHZ 6_j?,J-t< B[ȭdr1ueo#(ӋO0GDA	]f($=?u գGR7\1
q<ik*{hfS<F"K&H$N=WO^h>,<Unix
M "&8ҥ9s5`Vs	6qgHG]њX.沱1 9 |jZqFog|i$%Ȉ=.q>,r㕽wph;iЕW#i#,1Ʒ]?⯉z]xeﮠiuY\¨";R:dx&E\K?uq,F=OV=@u*O53~#[o̖ɷcuYM]6y  -|9,MTNIޥʐ
)`29_<+m@'(s
?	3otǦ_jwRY-/0<d6Z^ֵ]጑WsIxI,>a"+)YO^VLYE~u3ѦacXf]=`fBR=IMhZ~iTSZ7#f!/;(g#Ś<VHaBgs(BhbCqҊմ%i+y~.[oGNd5%_`	 (kզuf
/msx<wmeU.+i+O
+iֲ$Yé>Q:): C~^']sv#5)Sd&+ѾKp2:<JkF=,.騢:(((((((((((((((((((((((((((((((((((((((((((((((((((((((ۗ\ ޡkF9\$"y	x-@'zyw
7x\%r	`x8E q\ >׿dO|xмKx'YVn-d	Y\(5(=߰/w]+3``f`HiڷZG~)xS/s"ED#M>]4p#Ac<A_ۓFOɩxR:j7\iWCJ,KEvaG|}:w~gɶ |'</qXt3:jv	0c:?|m6wQ\\Y#xxw$P>HO;8 KYTF}
7Lv^dZ&mneB7vy  b_|Y.⯉S~=эqhUF>юS>y|1}wv:~뼚˿Oǿ?~^*<	]SEx&P=U^>׈ࢿ:7Mٴx_F5Ɏ3䂧g e?Ň	\%%u#g'Kf?߰w|!|?kZznd\'~쭷s1MŽ[k|_5D)4rI5%,5}Nq\׃?h/~"2w?	Hme帵egA,4qIw¶?W1D[9
.ԁ <g'ӯ> hЈt;k:;|wꕺG<k7!*xƣ/4i55tK;(S~rJ`J{_|x>*<1+
Ct\Z$W%$-w;A*G>:oOxwGtVCj[O#6[v=+~+~?"ouvCR3d]1
`5 	2kTvG<⧉|;S-iG$ѻipApJ5)e<5i$21$׈|A |мqO_Z`#GkX ]Y+jQX|-zJFJT4K:sj|񷺵"Qzͦ21>C9B]09=O}񔺟ˈqXuH4&U%3Ydʩea M|k~g<8t
CG4i6<nO#׏=Gms2cX_^05pD"p&<=Iʴ#w#/xsE͇XE_zWݸIYZ8!ņ	^1g_^K{^[[-Z<=o&ͅH$`q7zxA5[RmC*jq¶WVkqܴl]ݐ(9'߰׆t5|Cq"nm=l}X<1Km.g)F=ͯPO;?	'ĿxVM.\G8vHq5˷rU q >;~+R}WԤ%F%U (A
㯇utxHTF+n¼VEZزFڪ]6VkKߞ$F(NZ [khݏ<M\`9 O
dд(,dPd
&Ɵ&= 4ߊ#X!Dz-Ëff	)"} _ %O
h%6.[jl ַMgX5^~LoS͖%
	,q$aHM7S'#k<͟W[kZ"h]BqF)0L)ftuC߄V>=i;3c,ZDO^ÿg
ͧJ-P{۳i_O@ˀ1sut{;kx |@pkX#tcw,m
r8TNխ|\<MXw:u]	dsAa݈8k
⾖b4ᖜ$)*GFIiu_(?ZَE	fc? ^>$g4]$RMw"AS'JMhJgW~ jդ,u;O$TfzKFR1EMFvwD?
{QO2#
:THFpk I1jzM^qJ[V*ϗ $l<_?|Qٴy|ejQZ'n&0Q3FWXI)XOֱtK"QZ}Q~B{t?O_>;?,cʳҙy A5r?1ҴIxN$ΓJ 3n ) N8߁sbFT0	pʥz(km;$:1lg_T 	|	
g]*
2QL{n[#$v?GUχt?|+z,B;VYO
H e]s^K8P
؉	'd^kg-]ǘ#;5!e HP[$ai_^EO|m 
Z|F6
N-i?y|75k:טHeԩcq{VS,?#B$1cHXLUUFl185 `cMA|QqnEрcPsǮ*TT`I=sb>YfUkc?۟]}f E1lnRO-eǔ>z .4 KN~qpAa_{PͫrG[yf9ncFu^oi`-|$O2lzz$v|# ,C[CA⃹Iqޫ.Eu
aG׫ixROƍ:)*l\m?w<[=!xtXd>.c'*O\3U1RQ8*ZoyU%8nzU};mfܧ Σ?BkXn#%i,rU>-ҷv3sN%
-IHkhِ=c7g/Ⱥ'hݢ}ǔ̒P>QV8|;lϙ?.H¡;I 5sCĄ~":0=4y~smiUVO57{?0(
cGF6\vkK&Y#7-a,%grcjq$u]MnB.#С$ .:챘RE=Ozn}ьW4K+I3j-JRYde8#Lcsk_gO;.i:%ֹ!mWm-V`c݇sV<MIBͲ3 thn^漱ğ4yN^8޹U ԼQ%Pz-.yu038 3`g`ok:#wwPIechmi lqt]8ռM"V>ƻu)6*>Q~x{\Z>?T^I-}28$[lgb
᦮O+g|[}Qd*e~ȼ}˷Wc?}Ǩ7$js[f_T|;q?7?U ?2|砨6ˏn\d* 1 |7p巛fj
_0mno\[WM"!UYw'hsclsU~F<JpWlނ 
ÝnO_.=`a+ihąxAi래z_O%G
US>7S#|;"_UkzZFLq3ۀ}XweJC+N\	3H{Iqڲ=BmgFx(k4ؘ۪.poW6}VH@]c8#JQFV].m>Vl\M oy
Ce9ֳfK3
oaWy9T0:]߉Ķ^Hʛg/Cu8 )l#kHmL0´Q6c,
v(%Z콇WۏaoZ(XɌzzԶ:.l"6=GqGN)Z|V#ۥ>Sbl0m''9~4f$"Mw=3TX :`w#10d.($2#G(K-yZE<pm:N3dwQn˨IHV C\Tk<PѢ} &3AsڪǣL/<T"Sx_AG)4u]PgrB`EG\^IY
G'$SP[M(cY
h0#:?Z;t
2;}oQYvb{'tZwhnuMFFw%'=V	4K(dXB7a숌sݸ٬[3pa]tU/vlStukG,썦 g`B@~2Kwt~Ôz/42\mN,&#Og<9c<HX OXol-ꏚužַ,/tG@rK8AݻO/$BJ7[/Ԣ[Gdͻ$ŠRK
p[ >XEUӜd-w3n{^0Yk[\n U t_$}+[JoiicjJ#q,2#.Ș|̲Vn^> vjN9er_O,^"#=.>ԧ=^C{xXy!f5_.qyjˌyaH5-r;Pʎm^2Y"<ỉ6{4ۙ,[!54h~Q]O7Y&݌キOes 
4x{8\g/ٮCO&Vrcin	V"  4?NYMoj#XuHGr۞Ac uzom6e5ap
A{Za*+FHÖ=]q}֧aXc-ݭ\[`$F\߇1z|#qxMqX&]5,c.2u_FZ#&3|B_N7MflgnH,*[$hӢty7^Woá+jT/Rvsooxt_|6$)#qVIV!@
><UOk\OF$-n7I34Q$BGB. 9c L[w-Yptqֹ_CwBiKPtUAyS)N
gE8=.Cx/X׬R;$Wȡ|d_: xc▏}jukilaC /2-Q ?ltףyQg
Yæ	Ŏio4Ks,@ڵZӄf=浍}x#lnacӚz~K [,,bH8mx|9-ZC4q$7FxY$Sp&m~}#V`LLZ8sG*1XUJ0̣gښwFx"@U!kW,}|c 3*	?e[ >,	Rotג
yY@*FzwWSx;9<p|ueh0	t#ó(lm{5;C^MҭM.crz⣙8+w7ۓ^Gj<-;pO=՜ΕڐK!co>|ST}&ZcCDekb`Y|zv\W-E?26] 4n8zzdψY* :]lNP	"W-:_&nXkZD1*Ʃ[ftbF,zO-'~=2,~ ْC, 6}x?B(oeUk0ls?9F:gE~%rZFS'Kkv`FJj=x ^5Htܼ*έEm.Ha}y\w<$;XMRdrbqS꺗4x_]k̺h ͖$$3sNtuKR</k|L,"Z(U_D@ q jx' :!t)cI$ny*8+޻o k<EmuiVڼӰgI-}{9W W֛Kx"ž0Ŧ:qXlӭu$8c6HR0˂sZ9ښ9m6y=EֿckZx[Ėwyw-'7ژ*9_vj.yG]kR&D_oC<a6+j=GOZ=Mgf
|md5'>
T8c
7sGKF7%R %/+A9kch~#<9XM8ퟹ*@}Qn$RYӢ$gp߭qv|'nKG{e
we^LbSb_/xJo.r
c\69u}}?;&8¼HOX[iqZaotZM$6aFTmU
:ں|AhZY\#v2#_ N6җVh-omj4}ĵ,I1$I4SV6(j	3+#Ln_7b}kmo)ѺU
7uBχ8IjRIjkʜ$2r̀dC\jG6I=P$^[J|1x(1ҿ_	&48Ou?x^No$7mNC5F^z	[7vachJ(3( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( + m
g}r p6k+:g]*:{~^^!EʔZ3娥ٟ|": Gī{=5o.d[BQ6ds8p>jSiw7R6X 0?6zsX~,bO4;.1_͏.3,I W@k'krIj%zU!㞝5(>	˛uUdTI]v[	`StZD|	J~ҟ~	/E'H{}KiDnMyȚh7L|4`D@cp8m{G~mIϩmQH8VRѰ$;Zs L.Ě~VMZwJ5HK1LPT#=OJ R ho-~71x<R0\y.W =i'KXmMXPOPxFsxf f7
k}}MuC\]9OgҸe*LꏳW >4xKǚ~Oi&a
;cqu0[ؾuqo6Ć*p}c  |S}6j/lz6rlj/./xt(![%A7~SJ0J=|?
,|R__vlcź	2BAYZoKRn5/W,!KI.4YnNy=y>߆<Ek}P$rr
6u wI/
캌'Pرܠ1@=)PMiY*󓾧? b=5xMFG-XbumN0
[~ 0޾u)?j[[E/"B̫/'@~=k|Anj61~1$3"wQ	sar%ke6y9Mi9nw<p
&Oib!(WF3!?㪱	|:aZUhQ68[r$w|ǨV-۵KTY)d^*GuGnF:f[dV,1Ep<
%WTخIfw>;X.)LXMY`ْ0I'{7o kOӴ;_^6on&)Ы̧|u~hZǺ p|p*j	Ӥo7bx~'9b}1oQj6 Ԡ]Y4薭	$ͽ2:W]JVLu6v
sv&O#H*ȥWm%
dw
m
kt3<H>
gxT{TcMn#~WAg&[ !in#VQq4dۇ<{=V=Hm}y4 O4qv{\Ү# î}ICC{ uǶt,ɣFeD*acPz )ųNx
oWڏ/W&L#3"= Z]ކIV7asWgq]:eTE)ߴgGq^$3559V;	{R{vOLwds:<w|Xmb|[-2)=Or}\mҴvYUPH.b1ӧа-Kݵ)
-RţFFrF5GxCCUM%$D~<eG棏nȔZk	i-6/&e߾%c3g8=yC?x[̸[VOUC=>|	p:M!z+KnMq=hTzY1ڋ]}F>y:}h2s߂XcW3u
iὲ*/ u^Av9݁:4_kq\4ٰ$X#ѥOv6?iz=rMy(2
.J?|Ҩ K]^h<!{@a]`Vq@J]jnkyv hB!|$$jxŗTsrZ32y G.{+i}(ӫē\)w~hװ]hm2ŒQO
ia-D~|XO>'i3ɶDC{6ɷo*yPO'˥*ֳEkjd[d0 v.!z
i׏1}SdeWR)#qכ\qB'iO9ʼ,yຏNpj	*[o
M"I3OU
?#Kw/0g6ZAϯHQx `vnϾ8xZu Hܺ (Od1|
Ջ' 
Cߨk[٠(˯),a*{?& j&>OcEÖaREK6BF^]UlH§sbn?sØ8~4QK
}?;d>}Qk}qh뭐g8ϯ]TB= |[gIY+$tuJ>]s^숍WL#ѦK|x_¿mṋoom=7ti|?o
ɦ2n#Bڽ{$~ntk
u	aI>qҸ_[kch%Xǳ휚ӔJg!P&9V?c98j֛I15{l>UUZuZ$лI2`(p hsׯ_Ǻˎ	<R7`݈q7S3iZwH-ԏ&D3A?A<f5f$'}-;O.%l
jNQc
ē FBl,8<|0ykUMO߂^Ϙ̺t
)sW$;+Ӿ	Sj:B3Bpݏl}Mz?o}k[JE{׀|PB:gc/ݹ4fμi[~o֟Ǐ؛IX<+p}A
'8-_28+mC -<CY*R>w>M#QF89S6r7g;ϱk-˹G>׃+M]~7?Oֽ|.lw8+Gf#Vd;߹By#i2@~X5--)ۜ:kюhS26߷ $0vڱ\qn+26 &)-ymV AYOt&1U<#随t/Ԙ;ulsyH>COЧDa2pwOY.n|3n#G,q='*H$XUh_peFw{t"Sxc׊>o3[sqJC=ZjT,EQ mZ1oIך=C"$l	y={1)x.lvq>ՕLZ3I3u)bڰ'7W;nF}ѳ+ [Rr˵2ޟt8SlҘ{o3 /AFks.Sx}3}mX'&35ŨDcTpfw]'^H>|,kyV8 6  _Z&"wXmkb:rNp+QMRQCol6z]$ #'-,`]RяVN[E=A8oLq94zW|]*c.+QC>`E4
 R&dLW}jo$a}4lǵYHG-@[HmU}"sUNzlIf DYLڤm=$`nڶ#1\~eTkf8yׂ#DZWUZa*9#<?>V
[u	*W Ar1ZK;d8kP[FmpAvKVf[\un㸉ɪnVюַX̒yynK#}1cFk(|]߾MY VH@G-_|2	#Vt l6Opҙ%=:\\ĜsfC9=AVtWp|6jip?[X#D uj9tkQyk岷0dʽy==&6>T#i5UY$H0?y!|seG"vP\&?;z2XTIBLz1O棧Ҭڬu+c׵AIujח1,73(RRA9ucV:-CΎ*.\_"
@~c&t5̺uLPH&F} Jţ^mhcO,w>qݶhdckQ^EudfԢf&hzvi&X)\7?bU?;P=~jK2|&l}	Z)cg޴ʴfϚp#P~jԮ#O>(մ8Oݦ2_*\p:|8H|pp܈bXw^mC->Lmo7XM_>ei<\ [=4̗G~> gT9,UX&1mJn!  @)cww$&]ZuX%CHݶu\`mf#nf%D哯qۯ+D{сIճ}  B)U㻿:]tO	h~*|yjnEjG	hnCHv:WxKNiznXCjNIxiWM+v/%Ow6OkWWOҦr
f偛,]8ǧWO>nYE3&L_s{htMb+SnA-;a¯Rw| ×uM}#/C8"/O<7˦k1H#H<}YxM+;}&a d.UyZ}kcYdf8Oll<oYK]Wڕ$J]8C޸̚?y HZMK>nώI%۹P2GʠfEYo~RvJ1f8g@L7	Kg:ϋ4=K+}*ErEn2,HI H]r0Ҋr^
^KxMM֞׳6sc8
oi-o\jz[Hɦ_]:Bx_Ox#ú>KVU].nG
M6
V9߁ֹ_ |&RFRK=EO"ݴ@7M5媕KO_왼i2^ͬ(pJ]޵ƞӾ-|a5{xd7-G`A 0sӼ"7ƝZ鴫U[yqL[
1iA81o~5+vmH {u$N;w۔[5I!IAGbOEra\3sƞ4Vu<e'FW7zf3yN90V6)Ҭ&ֳR$k٭r׏ʣ+1޼%Q_5ٗWcyPrs }+?mXx?l8lyB0;PzWԵ5kRIao31Ip-I5~ПĭiOY-YOot4N6p<tܠcʡ;_g<Yʉk-ţFn߻{].]Ƨc{ZXy]vFv/يGO@sr"'QhY),p|_18e Fcieܩ=Qz[_xrXP|[^B#Zkf[}aRg T;ѡçGO
;5ǖRG(x5	eHd`yPtF:S%{IyY/r˕SxQFtE9JHI
.40PWps  V:߻h	::i#2Э?Nm&[L7k\>i$p!Nvlj>"WT7
[,",HsIA3չU;.v\fxý;fXp
.Cu|?c6dTK$ٞܶʣ'I7qC78`9N`%[\30=kzľ]Si=_bLI`ydo";ݷ h-K[Z5q@$`|p׭A;s3_'»}Z>̌>nIX}zӜWWxk|HFQ\EPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPGZ(omQQ6j?U(w~o[qXw46}DpsۿvS k㻛up  kuǚkr;:ui;}7Ff(ՠ|?o&M
wO(zS?c~
X!xQ-U<+USSMM , Ef*wKү|E?a246S#>F9'ټRIĕ
;``a c~)۰ S)eaXo'ա3xVh,kiX+1VpG7cE~khwN[6l`\~7
sҪK[)ܥ=A=.U<5}o{dw+0t9P?gI?lX9%/\ֿWemʸ6L8mO>G"[v;9Dr'SMH[nջ`9gCǥfVCM8%,1c@ҿIطzK6Pt1'\B[W[mGg<}<t'P3E'D b)-Spp0Ǐm{U"%u̭nxW'$}+ 7|7Y:żBNw M;[]ZHsP.#sQwaQv-fTgJ\lؖ=R`Ns:çֱm|9eVKvۗe8l8=;}A50ugz1o#]<ix+AYAW;6MmYy7-y?è9֡u_Am7j~
cԥXn"(2H&BF7\~Ōl2(̃
} L`/AOc:=(q#%:t%Ԁ0z;^!xV$;TfϨɤq]ݷ<E7&+fX!w5lqxWK8V4hn㝤k'ω>"P{,ndR BXq')ivZZIۦ@EΜ$"%Hr!S8lzKMte}f/ھw4~[~TQl'S|2$g;;{}2Cżͺb2=˟p}3cu]>̑ix@7?$y<p/gkP]gc0z7qٖ]RH]6ӂFGqֽH6zf6RwdHPk)௲|V7Rnm$`8q9ׯj4Rjw639%!2=<OVAᆻo68el#rx~i9WCt7$7/ohק)"]\ۦ[ Ǭy#(ϮirKº0 7kkwKڽT#+ߏJ዆ӣH䍄H
66yqztPXoiX
J<g=tk<3q3ܳ(6k
#t
Ry&óIf|37E8{sFW[ؘysH1`?-zf(ͨ9A/U1)9sυ.Z8w^BEUY8<SlIu8]CǾd7
 x
OM=$\|[W?+!ss]I|͙㪞1.Np:{[?!EYx~Zy:G|&ZѺ,:VcFpYF&<%0f{v^K	c]SsaqhWA 3sG(	m ?[s7iqW'@Emo.F~^7MuWut9pgP^dW/V=3I$DyHT^֊&OZk9t4-xT')FrH'},'o7"nch<kpXCI=3=j:wdy~x h'U"1:y0}+C@_\*Z[G+'"=k~}i|Cˍf[c#MD enXHC\*X~b9  ڶ{ܞf~|kLv<mcj_
4OJçAMV5vuW ٪utڻ3
\m6ͩh[A&!s;Vc0kwyI$f9Dj:k!чv|IkV}Ŧq8ye^~~"rs2G!l_m|Dj-.h	.\ \ {j^$n Aol	hSp՞|+{ⅳy&*{y[`^ $v51\xvV6V@IH5qWdNs$|Ğ].;(	wL[v	zū
ך{F?cZ[xn	%n_x|Skl4}QRI *~r 
	ȯ~(~)$"(- *8=\
Z Ǌ)P^mx=aU% E{/߃qIFCFG%n$1cV,#i/Gl
Mir+.rV9$C]w%
gZk>͸A G+7F%xt[[
Ǽ\8'umm
{VsIԣB1<0Opˊ0D>>Zr|y>YmA
H23AZ/Ŗƺ+oWw$vH2q@##me|![4l`U=q5l5gak]|iWˍW1Vòpry& 	+Z~&fL lrZz+I{עx"=5w^ִ]~0uw;x$=@:WSR.GOJJf[?4Gt_tkP"te`.G86GZųgH~Z|F5ռ_ wKLX0O{?USem	ׁ4WY02@

ǥfˤr7ՙڋ <u5[kyj͈?@[{w}!"+23rLqKvDߚǞsz6D!w@?< *qqƪ89~Z5hC; xq |[G5^?m a0xQ-m<T "fv1+y[ecq"<%$(/N:SgN9a*]̐$91<O|s@D݅a?~Tg3TjSy/zrd99IͫZke݁Տ'OʭILFIW<{c(wŎ6xc#b،B3Pem!x>n+k9+Ȯ0[|s>ތɺ37r9~Cּ2=9j+epr T:d{m`Ӏ s+|^[iVHY?4ouj(N1ԘԟŏB7cΆ+C*$f \,.x&dUڶB.R~=zvRx~ơ\N}o&Ed@6KzjAq}ŁSˎ~I6?"=/A2Z,f] YZÙuX[
n$#On9W-~CLV9c<a\0H{Ly-·gwFX@tX:vkSWL3]@?k5jCnvCԻ ?9~^Pc+1M~j[?vBxWt[5!)Ǥ;[
47)A+$6!|I	suwNTu"6aq~8YYX|nǖ[n5lCU_x}̒+?xvCҽI-4-n}éX֓{7N wؓi2|?kF.HYM! ׎A*%,6clVK[jjʱ
"sq%k'	zH F5YP7}d`p
	] ,';&lc$7WdPY l|EuUbiB7;:^utɋ!"?CWZ74°u̅H[622q[^ 'xfyAQؒB3酏֭Shtw
{`b2?W >oM[\| \7!>'Mҕ\v vx N˾/usV,M\ɸn٣e,uɌ-p }{/dѠ}ÆfcȯtF$	q hm܎{]=V>Tm<:!lsurj~W i}#N}Ra
\J."e l*WhQ^']k֩<0=xSnx^<uZx f|5bv:I0A b	 L
Հ{  ([=qƴi%b}^՟·^d"_jDm$Pd_cT~f썜^&췫p#'+7qiow- Kg[OrN#@N{}ibA`~|;
x~;]7WΘyTҿax+3p
z? cŭun)Ds[JU9xXu=~AGBY$½L}P޸}bVpR? |- `?GnZ$!ǒ3ʲr>^+	KV<EȮk=C"P9$9g>գP?U岅G |ZkfiG7?׍mzO
7J Ī߲F0[v	  #>4h\kžBL 2	cfAVOANUC^ zդ5զqHN@D6rv|}{o"jW?(O `}b}YJ]%&(?o
Isq W Ƀ,yuV_N  pMhwGk%b~]=X׿QQ%|ςݥƑNPFK(cEz$1,Q^ECm0( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( i%n: ~G |mpwBU(Oiq)93k5騨!Vd  3]U{/夑y~~M#Au#=ƅO. t__>\w?}kڨcI `
kbxf^gFkvx䑵b8\ޛ ޏ{YַZlRHht$`"j/tZ5> aiE4pjұ]1P#u&Wa֢$BV[I.~S#5nyOYʍ7~}"&CƋk
Fۣ_sj?Oo$j=-2ZU}24iJMB7Bt<akd𞠹iLf0 :u6i
Ƌ%F0͓?߰FO G?ңttnq"/m#Շ4cUp{F?|-Ok]|#b><.:잣O#edVR۱'35~ɞGХFa.ݷ9`?l|&F'HUJ%9\~eZ`
>Ŝyj2	AqieefgmX0NFH޹w	MGLh#TɖM.[<wK_OAcaEi]`(V.88;vs\<MXC(R.Y8 #~2teP қG"d,o"7X%pǌKJǞ;[JA>>4m<v1Г4}U*~t~xKǺ/L|?kUjD@	  ߯5$Xl㵿
&-s$f<A z]Ǜr%5"NQcXwظַSf% 1gd' mi~k(e:^yxqY"yw2C.yOATQ~2}>kjʰ[lla}џ^s?x._rWi܋zFZ|	Fе?~
a׼ޣ{I<&2ʤ]=Zk$z,<iDQfuD?U9V<܊̽]7q'W*dirux}_ǧ
69'xF4M'7}N>[p8`9Sn8{T_dA}Gq;#d) 'k˼k
9M:'%v#
`)xıiYU}Fp!6Ry_l/wko}ZMÔa	bFU)<Bv,7VyNP7/1AbR1'+do*~r|ofe#;&8=	⹵;dYxmC6 e+ czv`ry=npG1.43;mUyg98䝹u&^g߼ߝձېJycZg4)dm8AUcQH`UqӮ98RX=v;uRnu|A98^ǡ<W*WČuAnl8DH$;p^ރ4u-ic+(X@h6;9<31L.97*pwz0zeUYU ΰW^s۷:0G#Pv ژٴpH؛SlF<yG*:iZ7gu#sm#,ég #R6VH-ùRh38ίw>%,N౩/!>g޼IO[&~ 9<Oo؏^Kb\^1koݾf`Nz|%<̰* ggs[$}~:=4ȭ yv#mNxVsWɶ
b/^ UfPֆ5l$ckF'wgwlmv]H,i y;uӌe|8]2q@G=q~9 ~II.}'5_K_^pu.wϯZa	Hľ@*<Llsu𔗗bfS7te#~iG j1+peaݏ Z
;̻䙌#[:Ҝp[tYŴf?1,N9zWdUhmn'PGP/jzmL7['I W;ݾT\dQc6N	T*?q|$i1~ђ$R!ua~32/o'3G~?M߆Zs_-ߙ/!c75i_πk) Dvi0)v\iSB?
~yNoȲy鹇P+-[H6^%҉UILpp1_ֿ{8Xa9%:=R6ҧxd9vG,zW^o? emsgJ#T:WQ /%_HCgTS_c<,ӏK鶫-Zl
s;A Fw#S7=y IoK xMT9n7	@~]"$"D irtC 6<~&o0zqRJ8cں 3c۫.QDKw_yz*FN K|>IFG^f
ǢGJt&G:ѕ<+;0nnl1ÃJ66# bz\=+A pWJ?u2WW] m,*01P ]E;'í.eP\8:UFq'jQJWJ|\@%ƣ8
)5^Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Swњ (SD :u; sL߅ Z
*r`/Ҝ&&Yri@4	qLf[Fj M+UnߡpZ`^SE2'>Q@Q@Tr6?: 93RPA iOM{8s5%M+Y7f֘|5fH>JE:/-О !W{_eއ~ixHY0Wu͌Rkj2KE2Idj۶BWwB{: ds.wzO׊
ҶSS'\
QJ2*̧9yk`̮
A?(8 dOMł@es^}Ym%_8Gr9й|zp_5Y#iEu}{Frq #p7̶i>1[wp`PʙდAq5
s,dGaz7(#B`0>uyqka TrFm12%A+rYQ~;>_J&mUQA$
^a>s.
s<zt9|HV]#DeQ MX&t/^w}w-~mxzI_w妏̡z1$<T39~c/0m0OUfF<fZWSqo6;QSN{u :L7m#QGc(K<eʶ<5`f*
quYެeDuʟ@>߭qZܞQ,?AQWBe]նŏ'`Ӳ|gt<cods~+	8GnG5+\|~5,GT)rG?/<
͜o ܨ  591c5L[m0:Պfd:VX=W-	§WRE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE jJk((QJyPU)٦D}hU4-"
u C/ݨT SOOP2
`>1JF\¤aC. #橔T#Thj"t8ߟ󦀘to!Nt fKQYcS][/~uAT⥦0[Valy>P*
K$mXdE QE ƦoS!Ȫ?L$( ( ( hxCsG ~l9}
lPyuau1^X\©[gӨ굃rWڱO_»xF֠qqWh(~n+SD[̌= 8_5:o;?8s#XCtݵ|As5#McЩʞ $0kѵ0H`lr䃌sǚiIS#<vXpYJ#3&<KN=4wvq8 |ι柍m4-udUE(OrmQ
g;x4*JbΪFм8SЯ ~8hdI>ÄF2L:5=|T)=܋&&W,ȸLЕ9ǜJ&Cbq}8uO|JWѫEICh'<#בaeݻ\
K#3*v4{y=?ϯZI~lۭ:qϽUe˓sȔt$2I}?MYO ^߾_+zI4߽c
Ov* z ²4M6MBkWIXXI_kZ,V6e?}>7af|?#߿4:+ud[ ݰrfkxg;A+;v ']F_LrCWҗM\.7
8wJ'QJVƐ(( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( szPtإ=*y1Q?sʗS v*HF)R,S<RN=(@W8Cbo=7Ҩ$؟스g(JWo=֦ej@_Q@MU߉ufqU(o 3TSݸ@,YeJh1y4Mm"I2 kӫ mMG7̟ݸΣ4	-y hx_%ťƅ>;-V\
o<gϵ}Udyљr(Mq:8^j@6c<Ө ( ( ( (·22V _-o
ڬͩgxG>	j=BCG Q%*2qwGVm
+6mQտ09pA/L423(A'lp|4ծWZM>ARҐnyF;J#]糐Oiq?89RAS 59[*k>U,<'N5J@]ʡG\`@88~-xy%^8Y1aqP`KcFWq5G4"f^Vyn{? y߼`G+&^$PN'rzbXO*U2L&P[$ H`0d ~n}3G_L|qn4˩	
3	&wo|g&6r	9\|
?˳}?ϥ}fSQx5`{ROU^;W|奃N̕ڠSRQWv׵j6os\ qpk gσkƯ,30S߲&G,z}+Ք#s*tcdZ
x G<;_MzS-et[ȹ*uُZ?N>*E4[Da =Qqcck_iPplhq]8w."6t&-T]g5b6+nQE( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( )@
=*&c4p?X:U'J. ( ( dqm}jUyaum?52)nP":-[$\ ~?TtOUSM:3Fio8ȋ\Fo8Z6W+sRǥx/!_G Gx/c
ѹW<x}uk E}Wݠ_|-zG}0y5߁I̤mQEDU㊴Nr;/d nXyr?j=JO@
(Q@Q@Q@Q@[GwI2ƾqbοq=$o=y ?1z8P88#*ndu1ȨN3$*%=GLQ!&졣>V^⯄g&"|l $qc')|>T. }={^3O:mN0x`HwA 6gʋ_	v`WoXxJ]n*úC,1e |naOʿm]T|og|0i	l@23J7FG8AGOm7S%f1`
G\&<ʝiPorC^~SĶ6?*A$ $v|ħvU?L6Q:*$ rs޿R`/'.o^.VGytz z}bJki$cG(e .pK?X#IS]8|7/*-z.Lg%~g/Zta%l`s]nQH((((((((((thw|BJmtWLtq},qA9[kb2X4x<եo.F-}ikvZ'  *={w_Xkcl?emݕSзx8+<MFT?#E$ЬpJF2>WE+]A9cN^8kH	"en3._oʪRXBN(VN8XiݗLowº]å_kXdv  J	Q xS׸GXbbsY_C*?0T񗎤u}{IY<v$1&$\]wpH+L֛Ijj}鼸fKg%.ݔC#0| -1NW5K#*"Gu)ۛˋhf[U yCNTn$.qls\ -:+;WXpLyq2#7 W
>ckK躮ņWpm>S
 v5\jڝ+8o-H5![Vu$d&5I|7CWx"N7~2GX\epYs]'_l㸳Wz:8ee޿׶Ei4ms)>2w{O it-r1˩Hΰ~00wO><EOȨcݤ4W_$^Nuxӛo4]w}r+yHEue`#ZR3WF_-QEeQ@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@f( QE QY nX<BOC#4$ݑEy =	֭ٽeY6 h'[Í\A}t,gYtWM,|Zk]h;B[8]
] jNX]37Fi٣j+{(7R_=7n{zU# >5n4廵Žgqm08=x?ʧRUAuM> q#5b(] fJOFdmα/ fѳ/1M|: ա,³Wg 3i뻮i>H V  qZvi-M^|E Va?ҽڼ7mZ?$O`?Z'[~կJhmrɎW攞"Ѡ-eɍDbF$g*GN	l sIէnYyV/Օdw<  rsҮHY\]=XfV"0ȮĒa MiLH~p{v#s^ko;ptRHދXKzS4Un7vdi]ݬo\={_4(qQ:]M<icT5't&kx!h*jׁ~:[B|8NrѸZ=dJ#4QE QE Gyj0AW|\X
-w̫=g9r@6׹mWN]JѣoSRg	lʅIAGs GM"+E117*z}KL|(fI!ݴ)V$pFr99~šsiJ3P. 0s |e	|SQ4vlWB@}Jp\b3HO-7ٗ\=DkUmbR@G:@U4;?wJYޭn<C#۳ 	ii Yy|Qa3ܚÚ2CH(S^zܶC74+$XTejQEss`( ( m>?m?VPKev18E*1$[p+7[VP>U\~f/k,E dIwg!O̬3ۃ4e1X,1Yi3>faj/VWEdo;)/[YC
rېq3#HN+>% u>ծؚ TԬheBOsԞ@ z,il$axNݻl>GhX;e%7?;)ffSQڹ$N'E:d״BYԲtUV ʹg:otWVw$3
H*B A⿑OXZ
++h`$ 'hzSߌ	.lIedB3)"|J= CpڪNK4WL+J:gU$v'2O-jfDD"V@f,NAKfxX0BjJj(((*<Ek=Rɳ񝊣$ PJX=ÿh/۷?/Mk5F,$TebF7;*6N:kۇ
&;$:EĮΤ&I6۝O`?3~<~ֳxzjֵomt#ޓ	,a&
3i8Fpig9xaզ\_鳺EmwpOE9KDFã0/_Ƶ-JV*Zu5˻*
 "9 kϼAZŗWdye73YBQĻߕ7KdbQ7~WDӯ5-zO&k]gfAg y~P(۴~Rķ&i<F4y)q-T08PX)<-{mIαI%԰agKi	C\p+ᯆ6p5|icX/Ai! ȡx#?xajek',FAݗ''NwVGi(z?xEo[V\Tsc ۱R^UفЋ&pN
Wƙ%M}aP aX0%i&IhTD<V?1~m'=8Y^CtZOA-"6WP[n-'EEe9$U72F[N` 
Cr0B
;gA&5Oy43BHYBŲ#z8z>}vBY gqfl	\[:}֐CaPCpL6yJ/@#g_xV6ǩ};w>U\.	9c
6>b0	u8')?ǇQ}sAD#E%teerVl@gQWOu(ZmymeZ!$%b%LF  ?%AFvbUW0@y܊k:'>$h$}mk4&ݲ (r3 \6nN+QәHZ{6ܧI^[/l~0|5u=6Ko!JI:*BA`
zvFJJQEP((((({iKZ5c.w ??j?.nv=vZO,u|;{n@׵ ^ ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (4PP]cOQ~4 9ZZmP zW~
(˖߾^ ^e2fŷ f5Ù M5E׍!y,+ؾ$ڃc'ּ[q|T~DpB95Ѣ=q_?u35 CJ~:e3|;hhV<nYNҾvծXKtk+A=o&ze-OS7-]>QQfb˓jY ̮72}O Zne AZ߬_:_[U6[Q@5xA;E gY+~u-'Sfc+ ո2@
(
 ۩<߄sVQ%{x?7O F6sO?i%鷸1HRH^k6L JIA9ڼwj'W	m;UY nz?ֺh[T/K)S}!||ELֶ>D?ՋFYd	\4Cּ'oѣY]Rvg4csnuʰoZG7ZK5,v$u)WP6V1Mht6(Qp
9MCi;v+hQ÷r3F^*:пh|ܑ^~E .
ƗeK7%ԗ7JF>}=;msϟ|8t믶<#ޱqΣͱ+\iv s]x OOηoZc)@\r~G>ktqoS[IjsQE QE PNC5ʨЕɔWfmJe꼃̺Wݦ5,kY
ۃ#X
xkɦOYO\ך0ӕCV+.e,G*:ЂW|?o$gjgc^f>sJzF*>'+p( :DHQFI=_7	|(17m
O3*&#.:aB7VȨip1J@g+6Ϋ7F- N~ҷZu\j7ZLL"8PC.A8V>+x>"k{Ŧgha
:aX|8rw-|[>"R՛S!o&k/ǅv+lvi,egRт)|k_:l']ա@e,Hyq8ۘ k;i%pr	m)./M%}omOq
QK* WPF7Zgm5h <A<<4|<hva@blajʔy߈K}k3k]D.X4Hb9(dkPM̲4Drp}9+n=s<[Krr`t۔2Aە.^zzGcnƨmb|'~˙r(umoqkw/
^jŽ6+d'ZTP9oBuSyWvG9x?چv6ZO\1CJ#3~ /?ේ
wqMa45څ)̬%HF@`8Rr6۲2GJ<36G50;!xZׇ $No>Ə> GN⺊ 
~۲x|;կc%7=k.#} $VUÌz4( PgmiQk*w9_F4_+d
<psq
Q@qZ Q_:7
.^.Tnup+k ޵xkXlĈ lcvB"ϣEYJgӿMoq5:[mJia
Lb>?ݳr[mr><cRv,3Z=F<(7On6B*g, &g k&&nH4쥶	BWUdwV:oxwvyzK6VjRBe"63ƾ#^P^jYW~egF=2=oEJ#e)!|!m~]Z7lV.6	w<aGH6)"#~- 6WFaZfKbrD).u}/IЯ>g*-#(UlF%܌*ޭ8qݜR >Ž֞/,&]Nc, ,yaI~;+OoyԌ,BI]â~UNwDrr<ͣ[km <LX]Q$זxwwJnf1{\&NғG5lD#GqM\GJڤX`<BRF
'o젆$bbdN&vKԋ[{mĎKn-НTSj$T.FQAg'szU!#uKI=ͻ4)PU|希)hv6MWlkf,ہ  R1M/x|!LhE!n.pY/\h2+7Y8ʂOaTy)\b y<JNA=# *Uw,!w1
##9-=LZ$?tۗq1 nKѭcgkT;I+y1D02'Nc2}Kha-qT?Ax&KOTG&6Ѳ|`rY0rnȶ,riגFυsK1mh:Mջ̳37<mvvSr09ԗC>SMQz>hZɨ/{° |m*7.HZ$mgC'}ؕ-qWR6}WxYo:UadFV+=\Q]XQE QE QE QE Uj :]& JX?7ԡ_%?4P~՚׏|Ew7[2!_Ƽ7Rl^L'k|xÞ2+"Pߨ6ߛjz )Ҋ2nǭ|4֥O#/%}
kC-YRP*H>8M|+ҍcG });r ,&?y[Sɾc^5w1kJ14
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
+[ out ,}Ey?mkzڼ\[V8J-n{WI֭eE6j(' iV,kȰHyC}t?
n¾VYu_X?."-fh ?%
*d91^k}ߋ4ڗyX(F08k*"o;| #^H}.OnG?XjNU,ٽjqm#hgYrudx6o;I\ֽz(  lo2Ok
2xMf}4 ++&>ǘAʋHFl{56#(~ԴHKU//-KGsu,ʯ!ysX j#gdZ"Oړxޑ4v
?OHډʜPI
Қ\Ԩ Y.>x>i$fi]NKIk^Z mi۫m\XB|uߧe_4T$>$#*H<
7K5۱.;V%ukڔv^i7үfOaA>~z<73au&?Y^އl?|MkpIgdp3	ҫ eRo8??{ ۚ'qs*@d>&k" ¹oPw{#!pqEx^xK会I@f'PW+Iu^ _gw4
ޢ`gͻ'nI  MMXETJamtg'˳_E7ҾNuOy /:0 \xs~	Lɡ^[.	1se-lg8^'*~
eM(
gn_k-RkpwnoHgsCGQ[ IY>=-&kRc]G?| c"[XfrGb}]<U
_.{Y!r#~S|N}jU%U`}ݣ6+&
}ǉ~7O%iK/~^s]u#&HeXcff
'SvpFfR29bQ[n8oJϹm]V@JO+*Anb`# J}QZX#(a
 -A#]_ksnʾβ.U8-mks O )o n|YD`SW7?qhJk~ /_VWھ	~e(68 k_cx ()QE"W٦aM LZSeR`-jcv2Bz5Ggo(VzΦ-8;\s7$li^wf/ڵ\H^s>o Vza-2 YG|sW(,}a%wV2ֽ/w m쟼=~GAY֠jn'{}߻JWљu=uo7F?=n*~ҸxuT0Ozxw*vqњU[MZaԎqmk$T>';Ěz:l`Uy'H^NQF`~_LeۋB;xzu>~F~e5;g}gHҳJ9AJ3"q>7qSXx^8xxwψ,#Km'`Jƪ|d_Z&I$|CNxR
g~a9\4{1`ɵ+>pk|Gŷ2Aq	#NWO+_ʆNAǏyIXl6&U+0eBaSMRNM]5;oH0i6s
X;c\3!VlpWh#ǎm[{՟HyOO<qF/(q@< ㏍^4R`Ӯ6ߙsDayF,F4>OjSY]Ik-(`@b\,XV5ssNˡ2?7O,[a*Jђ'em廑/C[U턛xg7:!%N̡* ^ 戒lXEuop+2-|+tjFBWx _xrdtOPt	-yy%#n6O'51EB5{73M9k6*VYc!q*9`3\akaΨWRI}c:Iޡ3"v\8y<gν,<(nvH%s<sZnr#A$wT5n*Adg1|ӡkzUC47h1~f~C%XMOŭ7'zm:mwi7b/3mʞA `Pk%-I\}3_na>r奛$2,`@vhPU@IIEc
es
ȇ* 밠>%#ˉFX&WC_Y]S
ݰ#' u.ks㦕 	^][/ڞྰ7,"̭e? ǉ|O\(&M0-Ùja+EAYyL
~O\Lw~0K`k:+{n$,@EA&2	R>d;?N9mBKjA[[c_
 A0T)_es;jM($%SĺjB&>WKy|%˙[2s1Wşo]=w՘1^O\i `S7F3|
'Ğ׭-^^Cqo6q+"fK9R\MgxXn{dU݆1ToNJap.sKn;~i&Ԅson,Qcު<ʁPToiZm$4B#XrVWPx uofief
(\o
]-4hn-#i*u@
zd3_Yija?yY3jBGo+f0cI|?3w$8 U^Yd 6U\zOI]kČc[4
p~Gȸfcw3+׆"nJڄd8ˢ\ pXqs'oH%ۃ6L3*Ƶjze7zRIA0B|nGN6&E%{-u;[P,b&`zvt9"VV+ϖufXܳ2u> <wO2t<#qp`;Sl溒ˆ"nh=0m'ȟ7A"/lH,{yQ	
0̝B 2<̒NKx9˒yV `r	W<vS[%̋bǸyn~P܁ڼ7Z,v96Ȍ(
pX2U_[M8C#?p 9&WjX+yl˻`C #3*a.鰨9T|؜p1aҹthYUmT
ۈz
>5oMNT`˹3~=/8Iky'dĜn"7q_$To>Zyc\Gm}ffm@y|Pr+sϥ]
o"qF	#d< Z&mK!K6g颙e_#sm݌WCQ6ǩڣ"ɕH_; {]Z}ȷ8m
&#$$9#881tDW]\ӺQE2{B@WP9u	Y|@,?U?t
-ht5-IR;X\騣4P ( yE mZݧL?o@߶`Ϫ"'¼BSΠ>c 꽟
 .=x
.c 0 諪JJ>rr=$cc V }M|lY  ǒyq c=LW>zСJۢCZ5EPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPMO*2ǵ:=fQ?=-ϋ m^k^2V9	b̾^?kaU>AqTE]~"Iqi+Ö? kBٛh'auͼUkc'w2,p̞@fdbJ >,ccr1YQG__/
	fsֵܣvgV*24(p)yb-_mk/*s+02pW_ܬ͵dWmz~U#n^V1h\qI zu"ҭSzsT *??
=o kh୫5\fuVc^)Rۿ5+niu1IzՁͲ׭)&<MET	cjtVp-g|MBqR<o"K"?|C οnq>7$/~Ggq^Kmŏv?wT\-zy_۩D_J֛~hvzZ]lʃC Sb
xwI@;PR6 ǟǻj#nc׼|,$3Fx>{0iBu/0f]} }n_߱OmBo3knVV̍UGJǍkumNh
m(ʂ&T
y򍝎{"_Ώ5q֞.Ԍ{,>P(+O>#ڍrAE\dTrs}bxcp[ /%1^o7כ֞2Tf[vVgE.[kQW50|W##ZKsl>χW  K_Qh+XGJ7:T#?/fb'Է<{Ly'?SÔ+t3kvи)3[-Z繝S\sh$쮥@{ׁ|I[UդЩ~$[b2z|3I|=Y$ݹs,¹q:S.|OkWh%e_0A_G5oV<5Ԭ⹷'!q r{˶|5d]x35y~㞍&>"vbHsOet}ub~vz߇lccm`b8;11|Wꚛ\xo(r\5@^\\Y=Z 0D~[4 3ZI|L<(h|Jz	6߂Z!ȭ}ShW_OK|䑸?1_WisW6#җ7uq K@L7
 :ڷGI$XbzxN|L|)Ԑtw?>|(Hʿoq"q\&uTYjn?,QϮ C,X
 
n uAv; A51rX~q~KǊֻ̨Acj5/ #^o+"Eb=z.5fs/ɓE"?_3F̟ 55/oG/n W=R/Vjk41[`qZT=V  Ӭ OuU6  _*̧pm9ŵޮ=<x''l; ,1Z{٭}
|VТR"Y.̕Mq:*l@Vfy6aQ]>^fgk:<
w}j|4IuS!됻8a_N>a](7d=?N1Ǩ:iu=rY;Lr(e5zdf]"K/6<ϕ]9U=uo'Ox'FPVjk2>=E\oԙ+ij\Z7/]BK* FnF?L6U̠zdFV>c xok_()ݶGWAi
?+>osAx%Lv-6Ie'U91</(>q=1w
gi`M CXd3_5kz֣9";ɪȀ@ ٜYFz~Si hVļsY0[5Đ[l1AlF6Wfu$tippv7zWi0k}.v~3 Xd/-5ƥeq'䝵+7ifF8v#$HcunFk>u7sM,cv2	fbʌV@Dj6qSu%cu{\E	Pq}̖ynBc6AHe9}}kh,&bEM$_5aQ]FS"HFGy=巶$s$.$1yA!$4~FUV9wwkN,,Dp?bW0w_p޽hPNS(J-aZ(}muW6<nѤy
NnrכYXjYzջJ4`p8}ޱys;E<Ǚczn s:M$ɼ]~qf 08[E֨kĩ42y,bMBBJTBI|1_i+9yI7Iϻq8siJǕXűCzT@ץ3U<_^{?Nt6W)]¿F?m{ET,֚,Am)>eC$n>|%w1d>cI!s Iu=BTfF͸ιVގXˌ7\# v/\o^l*qۤ_z\Oq| ?ۛ;ˆ;*+n~${g5t
r
=yoo~uP}*;h!m*]0	'8*xYӏSdVWZ$6ɩjP]v7-i(w*
Ʀ0#`Nsy |q?fkd{>ԲZygՔ.1%\'牛C5;gԦ%ԎrK@<p_mmMj	iPi<O
eڗ_fM9*>:7}cg\fdEbKUI$eIl>Ѓut#dgYn.H'2W g  A{ѯ5-J	{d Go%(&F,B 66nlmeѭR.5YwM-*b>MM]aྥo]X߆+cy$ݖr
4ʸql5Ju %]U]ǘ奐li,9hQWv+-zq{.flmP.DmB˔KČs|m)$&hQҍW/y/$%}՗NA6uZkm롴cdX>/z=o]Myّyy4+$2ʂ6#p'[mTF)IZ{uRFV] ,ǐwiw\^GV@YJY\7*mPcpp@	5j,hm"j~'#(Гwg5I+ٝmMkNnjַD5F;) FIpsp
ē*zd0{ro_E}͵`O<Vx9<cQKw#xzm9VGr׭KfGܡG 6sKzVx̑+HnxN>FHRhwO3]Zj#!098ON極`_pT_lӌZʢmIqљZO29
c'?(	bx{'c^Kp.%1o&,GN.AoE4g(C2G+qs[m-%lJvyb l#<qH[A<i<Ю
 q׽M477pW.+T@Q#'<dGq	,\gv%x>/!<wQL˻Uh27 pxjo"f1<NX8J]=}bqjpIVJ
3v'sfÖ~7vz]&ijǿl;18BA`#nztFɒ+?imt;&²h-M|2n@-A'kㆅK[i5KT=؜Ws  l9&
I^:I#myBT;nG7bN}
=B=JJ7ktpu3qZѩ0=5~l\|H	'\|]qjǒ9}?gz]]oN9j  2QWG1c_ۚS- mSdV[柷]I&ԲǶeԾ?_.ZⅿKҢ6ϱ)mC"ukPs$Я i >"UeX=FkO+(G%=_Fx?uRkdEa~Qq7soNkE}O_^)jKMN;!OJm'Q?3nkѼ:͟?uWY lCVJ{lI}
C㾩"
n'x_^`^ߊZr>onFm|}E}E?#gR${I3=}V??C _^/Ĺ2Gד{ygS?
Tuz\iN( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( o`M!5W]]3_F56_+=\O|#ywWS+'_vxmde_}h	ltzc$nggݭcz/Xykgt
\{q
1M0UQ*JG$ۻ
}JH}#2]l{g 
-:֝n.la*I8$|nq'vFcM{Q"XMry6umRwÿbi-#ya~ҺsiփcJM}QvZҾ~=OM czˣJQng]2I*H ǫ
?X_qD+gh<WvoXW&Z#k\51Wc4c:wgO-\=03k|gc֮|$k9ZpqS\i7u?ٴӣ-+I189ׂq|Rh$nu ը2rqǩVkx~XӴDYͫN$oyO, `¿% kOi~,SȪ5h
Qko7{lI{ʹZ
i9ï ]xx+W|{:e n{o2?3W$xvG^_d!W6^]fK y{PgrҟĽL媱{OC jO
}ٙ5gE?Gv 8*ox
IdUpR\-}+HGvW¾
m_wtz\3O*@`VQV#='?~,8uR~Y#> 0sr^J>_363`qw5}_,o"ZݜZ4\y<I*>2(5ko|O-63$OLt= 
ݫ;)&uGV촶b/=a+-+=W'k7W_d!`qy?
deRndI){5ucџ~~zi7DWw? 5	Fǰ6~Ex=7K⳼Դ[m5G*yʱB^#Vuq,˫`q Q$.GSϰ;ܿ# %kiu4H@AcǭyG S]O xRd;_1~*yk
]BK^E"{7}9I~xJhQ,ر)>
u6"HL*
[(ߐ<kǿl;FW'9,wZF@i2=5ň;?>Ě*){F ǜ׋k$Hb]^V8jla^G_zn]Y鷰Ae,ꨖIU9!S'\_?f}znk]bUo\ܪd^ƳN)-LEǐb־թFwl־7r,lz`yt@א"Nhɷ^SI.tJYJ2$py</<)̺}%pEyi7
8F7*&Xȭ0ZQmy*Io~OZB{M-察eA8⪩OLc]3
zeP_
WKә_4#_:}Cڶ`rAWZ7dӕ<OXꗐE1v9@-Ѳ wimouqw_	U܇#i6qk lˡ>g
+g
rzo|9\+(Y˲G4W]*U}w'BԜG5-t[=A=wFrw*IyCڕnjZ}*fRأÏs^T[?l;QA XsK4qM^'i]m#ðCeB^1_-
F&|Vu<_i.{im$IϗדktyE"2|n:RSN\;_# <+©dʠsp ;=OygVFyK@) t3N񬊞dcN/:^4^s<pȧrpTyw=J}xèT-YD).n?
=_>Y&}1ԫ)r{׏ºE$%Y;=fG)v~vj/'X#UEQ.77k{IV5mWp0je;!`#~7˩?#ҹ[mgq9ˤ 9ǿj{;\g-)vuq8X{zQzCَ+c6.YeQ:gúe$ϖj-QK6n8"/fV})ܞS {yX->:p3E~F|L/|Ms^Z̶*htAo
\6U*Te[岪s巏\ ]ѷ~,~O>4zu8xq -~ng!w=~k:e]j;:?t2o
CKEi*Fa@Rv]P9ω^ ׇuu
oBVvECy!^3Di3GM}@0!xWK}#OK5|s@T=ݐ@@d8|  .5'k}Jѥ'ۈn)ۤTU ݹZЩԍ=ͭX\kfZ];ld'  KYiRǦCq|pvm%ZG
@l`7>igqcl5P%y<eAF j?G%Y%xOʡas9ޟ/@Z8zmy./<}h
"wm,
]wA{zms[Y\Pͩ$V#)Rڻ^	aZ|cv	eX힓y&(ؔO:H,HFlᔥ} <7(Ŗ]>'ƚ6LZjhb7R:+,PBB˷0b~^f~d|j|E?:_Y뷓ҡx]FZ\2Gd
2|~MOUHL:*U9دQXiZſvrx?mjea{ϳ4&a
̪cFB9 9çе-wXw)G{DJw =#4a2J䞦4mW>
D o^b^g,
ᣅ$# [5~?G <oṼ3c_QIkmrLȉ\+k\s	o?i hm*=k2H{f+P=PV2 )vVt~[Gd~3t]>K jĉ3@X /w;UFB-9+*?T Nw 8 `W<v?h=HG{q{洧8XJ[m̿gYg 
-5kHwsr.ž*ʠ'V%yH"zE;{DjZ	=cŗ?u3K.kf鸉־5>5?mE?&R9mvJ,W$qH	«0a 'wm" ] J.rC{k5D]瓜hZw:o<A-6w`HF³1,ignKzfWn&8bxnCuJ2F0A_MwZ9$mMY.$[rD,!H0UA[>!hz^lu}wkŎ/7hcCciД*Fku)]XށYi:\ꖐ+^KYXG!,ʑ6pdSW&xſBKYkTq-Ö2$k!
3QZhuM267$SkucǞ8q we>6Լ1>c^52}<!5afȌmv$ZT:MI<?ﵷ[Kr[Aorqnһۑ
S 
rI6izܲ$)  	= UP5%YX]|qڵÈhq̖RKV9[jhwB1毵p+M[=IU2>v*̭$gOGi-KyFv0HKA,0Z4AeX^#KdIthkt-m0
8#a
Ʀ+G#eݖ$2ve[*Ha|0wzK&45l|RܽЁ˩yXrB}B^#77X^$4DM[kX˕UD%N[v}{㏜lz֦:ect7 ͼߕ~e`z{`u-c]j-e#xd)$nB1epC6	CQY3A$670jŴ!T/s<p>NlagfcZM1]fj 89$_Z<{alˏ f*c`B wi7mu#jlV6\+$X ե`@V@5M;sT:[Y̮BkE,
Mp4Rn dqZLīp7;8U\&Ȥ03-"ƆR>Y
ぜg=tXPm䜵QfcgeViSno# `3ry?lڡ F:~NjJz:/P8i.Ց6(?xںK[EҞd!2r~

"X
M
$=rqǡ=knSj_5c;HPǂ2A8lf\{,t a%l4fDVlJ3܅K
%<~^#ԡFvnA>ko&}]0ICq4ڌ!O@dyA8l".H YG5' xǗWSKqkEhLqZ2jgN^aJN[SP3++Z⮊C_
:o3ͮ~ϐ۷-ݵb.)L>6j;B2RWGJ|{ogw{M<~f Z_lkyqiFmzcc'. >k뒎6Vҧ+s[A*w(. I<E8'?U?9|cbm3nW3 4\_EG#\ m1WI WR
FVe/5ԑr-+ؼ%?M^>lBy:1+4Y|=yg"PD^wи M_m.?#A'?GũC+uƸ P;멲z.WڅŲo 5TS>Jd{ |Ʒo"?noa k߄mK?dQ ߰>%^/#n ^>8~m\uvxhHךwQ@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Cqa51V]{ҚJDц_YӦ ve87e1B(uS<bOrn #\wM=m F%n5m,?jrl/r(WϿZfɳ` ٫ Aubwm+k]ZmG~:1QVbŹ\b۱S9" W#h2[k
1CT,hԾaKgeb]w=ZTig['ğ[չ  I.
\եُE菉lGs'v+ R15% rj?:q][` 'g7Rm M}W |SzV,sד~w L L fo{JoW[?
$r7gƴL}c/߿6 JCnl7|s\57_k}={r?%x[ׂk}R^=<Fgw0355ޕ-aO2u}>2K6*pTs+}mR)Z9A2?|GҺqد(tkЌq83^GCJFk{f89ok6vtYV}1#}х
Qm ںij>ryr>
Kё[̌?Z/|5ĭBRyQ֡RC7 -;ߔ"ՠ?d{4fw3޽k +tPqCۧ<T^9ax/eÂ8 V:=:hyh/>(j6oWeО ZP_v}S\I
is'Ɵؿ~n@۟Wx269ψ2Sq(\RK5Y'y8<~5|DeY0Mc |d6$?t㙠i<G8dǸ_AxT f]rr\>0WQ,3~M6]!WcOm{MP ~K+~F<.} 3^E׳jS/.,`d\my1޼1iyv<V6]|$ʦ\#8cvMe~>m/wa/c`pr9<H>]"9'6k T/%,׌ޠlLooج<VǓ EuK?i+XmQ#km%e<ןZƾ"[Kt^dQ)~෥{uԮU
[Òs{x|w Oy,vb!Ǩ;We(1f'įGt-!9-^yKGoquocbmV]e'3t^-GMVXg\#)\ǎ~3h:6ŕm%?ƻGVݣrNxT̶|}-/Y.4UFİj1qƻo4[g̺>}<wzVp?z㶟mMZWA$(' ~/"Ky&A+qstpv{xkcThm\)O w{5|K~Tmhf8-*9u>Oÿ|Z-k/-̤@}A{5Ib>͏ZaqEz
QV/sz5U_|Pf5~=^]kwoIyjYvӽn|MyicZhxp =N=pEs>1ѵxmaiDaFnK+Hv=yC|!fb߼kμ1p۷7֧Uiq}[p&< f~1?v`OxʗOPl_1_s|[Om p.v|[òx.gV2 :m1ƊQ@
ڬgN=MMBmMoYk(sW5S1ݖ>rkSiY>Ϩ(,( FWrʹv jjVaq55:f}{T$Jͺ/s(ȢTpԔ85aAQ1q@ҹ59ihtewp\37MoĪlVm<f˩QckG䏡5O Okߝpڄ_lP2V,\`K6I_Jh%XKI$agy=kg˚W?A1LFej摓.+GEڥ鳫Y׬d6	" 
  ,lː<~_FKJMggg,"I<IBч$0_]uX$Ծc&UAw8(!F3~m5Ѥ_K0hb_|STdN>A_W?Wďo	]io|?Q(!v/>PxY%P3W&w/u WoxۺIkulͻ? 1jgs1 |NǊ5ٴ%W"t	pf79`uPe7SO[;{=CUE,dLm`/{#gq%\5﷖1}rUQYTƊ0vc~L`W Y7
sC߇fޝYU[d6o$<: ~
d(CJ*4c+].T1lE̈A~t)+xGUM1|*|v8UL~Zoh:uݯil˘Y|Ü|>䑤b*dz-WR[gU󼰘/܌gke2v,; ״&:?? 
{[IC<m;Ye| 5 76fIt d𫔬i1o
jwZX#xצ^_\y}#59&K7_V]^vXIiZL{එ[a"u }c8jTRr2x.Mۼ)lz1%	L9NԵ}`[Y%҆l2>B1mW"R;7o;oiqqOxbsGs߲ |=g~W[Y$)-޸J2@~B M麍ݵa5sfy+""H΅QEC.
y<]i6,}0e fX3GBAVE'ߴt|W:;X嵴MhE6pJ!|U݌c'? KڅqKCrnŤʭ^R. r@#VTջ˩u
HZKma14Y_EQK܆2dVظ7ch=MlXݹdyXw#5k_ix t26Iv2}Ϛ?*K/kBΏk3[V&w!bi^N<23[0W3/ Tׯt xna}I3°79*3&@
yY-06-"α,-|WO	[_M,rBэ#0}хUفvGnA[
;hĻmuJ8F1KtG<%ca05{ܨ/u|?=nTP$iry*;L)ǖ;
0!TZh9ans.:kOU]Vls#+ݫ}fω^.-=:&Y_E:	+F8>S2TYb7/G zuĵ]F~:wo..5-.\öW%~w`Y|3	;_$Hs+?kzz_uz]JY#Ŋ8cTF%7qK/?+MPSgM^Y%^M줈B,J*='OΏ/楦כC=w[ޢ[H	Jl cMүhtwBuW:NX#dTH
K%U2HfUT^vd ݝ[,ZkԺeRɍE
 *Qv1OoۣP5]6}Ķ
c"R$ҍsu2M#fPɚ̬;"-H,EY֧N:u ˰c(]9Gdsڍ|5沆jV_O*@!OdyvRd' Ca%K
bͺ}8)+09*21IuthΥnlYԵKnacm&@?)
G$kwڧk\#cR'$$׻A>zHZ]\7$$"/$dY\n0vWR	W!^3_%K+[{+ˋpek2>	6#w~F}fYTT"bmc_ENnXVrB[cd2;NWr+{G7V^C,л8o-y6*G@q1&m;|PX$>zmwwQğ[:FwjOtT'HH؞>ӑSZY܏|A5v|JF&Xdfەz`s<}qiW{ӡV8~Ş fEU
	t<ǶBʮJO$4:fºy+Oy,|҅cO&fk\k+9<oIn3?Ҿ\ rϾ.u J ߍPSzNxoNo.gpGnhp1m q]I]5 jcWv7hlWo/,[;8k??iŮDXb	hf1{8	29J?l~~,?]K7\oo-%I$煍@ ߚJ" jTXy6=O
~ɻk6v}Ԡ* Zj^x7eVY+u :D,uY4{f;|"7m?w9lO?'.+{Y4d=qNq+ugD~?˔]U]9_ݡgn#|R8}~:| g/-IX߼S HfJ'nڟkkTu+HhV'2g|c_0d{kaOscU^'ؕGğ O J_ybE$Q[?^׈!v4r1JD&q> :~9^(QJ6ߚHPf+5fٵVyA++QHg	g["^?__~G|ޱˊUu{3-}k##>{,X Ə_ օy`QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QECE4:Ɗ3hGcj?ߵ-߆5-|ج1_X>ccY`C@1T'𯜏54vqm0@1h$uq^}lUhuyK|5xM/Xò'۵7M'PL*:4p%帍߰~6
+Nz|%xrƵQVdS^A带r1U9 IP0HTSZb- 嵟g0r\'_c\|E&zWv@ZOOdf :/$9NMiI~2iὺic<qPI	L,qXՆ_jt*CbhkZ9(fz#o÷oU5_/,|)u=C&o4U]g_ky_Gq$f!0A'\?{uI-H
KnO( >)OCj:<y/#O1n{(! ٪ٯY7Io˥r+ cO:%m&$.ٲ¶?d?B\;H|}8 ǳ\
ޣ;dԾy_ or5ǐ⏉V F}gA~S |@2+ {ӧZ(jG$h CRcڍ dlihOuxG_li0ԯS9qG~nx` jݼVq ޿Hno¿/~'_c iK^L>&v7c v66ῴǋzlnV 2SxrDdo3yvDZa29֊>%c¬h_T||O^7g>5|^t6:brƭs撆=r{G3;xuHʰl~dWGJv<FE#=F)5y\mC>so2gk~*֟ⶋX
·kcg	
.Fy"~j?<9Ek-
X|~?Jco44(t֓Cu{)Pֺ9Oz	Sf{D #tllbBmYOzVGͦ
ys ִՑؤ=q`$|}B Cy4+s%")xq:URi8^gx.5
4Frs)Z^GkiRi7ȿnZWd#N+ݨhBėȬ񈴋96ǹNq?r7_:H;3d zV~umɔTcgwG4Ri8?8QzWIkxet-Zܓ"n|x]65=6+#V#=+۾.7Z=Z[^C.RZ4lҚͣR>O']זB#( ~5A,zY|]xvV(if%8UA<-4/O[ɭq:n|q]>(^tiͷwwnUrNNO<חS}OR8KME~,iڥ֛uk$HMo_ CğO#+I<цn.nH?VW_r ^Zƪ<&͙#lH#y'ugkG񧈕+i
~Uz$eG; nT7+*sɳHj?p4-2p<k/F
gMYFu;͸SW]N= O1*UȮ~8>[CV=C e Z#:IK:gU:ۏGƳo//qˤIpF	l'8`k5?ŭ#$l\ݲyzů/n/.[C,ʙ_= J_x>=9g{
OfYr |vƄcΩ4:/_i=ҵG\w/G*U=+/]Z3ƚ]Pjڮ~U zW?XxSgs\iYe,?to+jWCi˦#mң[N@*S徥[Y:i6 ddd -dJu׭-R(I
<
q:('g5_mt;aifhe1 z9Z^៏cIc0YC 5<4g{i%5mN6gt9BAs|	mLg?0P|@]BZ3hAv#g?O_'RԘ~=>w 
5k{+;DO*k
Ʀ<VHSW1N!2!8'@zk+VĚ\FXPUQG#W%]i  ikzk0X9<2OI-6mMfHn@$tϜ)
Kɛ?r^ }Kz}|K@tv^
?N~VcΪ*{ٟO.KƗדQo-_]]KB_f'VǙ:?J͡ǿq\u.k#?r- j<ՍkJOю+CFM4"e\w	Jvg\iq2h;&+;6ѳÚP-KquDF*o`}!f`$j
-s+I/$SC/¶>_ÞFh?}I2
J
 ?Bq~$uI4V><Ŕh%
՝>z7*R~7់rV oCg=ɥkHx[Z.lu+,'T 3A#¾ %Bw#].vbb_H;Qx?LOA]rJU7f}hB*t,wm˺m.9-.b
JG(9hB:$O.j\-ِA)qjɴ
j̆o*Ƽ|׷CYvіH	8gm3oy/БYsF7/u;n;wGnL=Z0Y*x	˹Ͻp>!w --ssXz~#i6*O,wjc4UV
VFo8Cak%Srﻏ˭ x<m,T!p\}y?Դ'#}>QbegO"15#? =Ek?TWn0]]3Kp="{ Zċ4#3L/$dGN/ whP}A5(I3 M}+˔k8mvO+\dg?ymf}[M7Wpyw72o"kz{W+u,:ׁ|$;>+ZeI.e6b+lh-U-naOPd|E
&	b.Ê"u'OdIo_9d z 5fQ߈<h{j
П1u ~?Xfy뉓]_vtvSʝ>j53~Z6tkȤZ'Wc
 <bJ9c]wn-YmJѓ?#z{;MOkF<e,,HY.dc$Ԓ~c ߵᛅ;+׮kktiڄ:Nqa"<dHv=paVʚlʜjP_ZԥY$v|h=G=SG;OTҧ졺m6F  m;p1<3;/
I*O]D!+s<J=l~ؿpPڏqxttaԿm~3߂n晼ɭd|d_i_xVOI*C#PJ3w}߇v"N{N)~X<qEn2r_Lӧ;¢Z2j/,!K_Y%6ֶ3AslYwVoo3t=X,uZE5۳ys4py#G9$ H{
':)HC >.{W:mMqm
Ge2!<g'yNK?+5o"|dmM9b5le@w. DFKPt |Em6.ʬ2[. PQ87o |S?خx{pf[uiUلs1`?m  c^ky͒H$8<oe*ut~O^ꚗJ+M-qy#Eb	C!YDy
Ff}*o:sivxF6"m;m;g#qO*-+RմA[{kkj\#EԂ  `WESߌ<;ì6o,LĦc.r Ey5>ԣf5cf_K㷒G{eG%޸ j/:C$tH7֑^"Fc`31|xe /ml[- rTIlⅼ)=׈'>րvv` 	ziIGJMʢJ/)TJs4`x^ko5-;#hs8pBR\*ᘅ8<i?Qt[=SR5w{hiJQF݈$*`i %uy?.|g4
h&	%g瑹tH<)|A8~
GOm[c
'-Zy7h68Tڥ >I$Ij|+{߫>'I4&P`؈)K+~d08sX:|%
OL> hku(a4"~O$  9#> 3 h/1 -Qh2X}YcupkmþgO/q?L񖓥|H$QPcUX$7W|F|YdZ
>UuMWB|bV;uUdN$q_O|T|)lԴ
j k˨ο0$6q9Bl;YM
ŭNȚ9S#$Q(j.Z^|8V]t%/k5MO~*:_i ٞKhLatA"H} ?c_:vx45&;md܇6 (
$u9/wo}6v
*+Ȥ 99Q$[+xM-tדAv^źWpss׋,uZpQ)Q8TI6<7@8 q~5 |;mywڔrg㬫c¾MԵ_S4-Ժd0:wF	a{!>{fdeFcox8?uCHyolԷi"{mR hh:0*$RO dqר,дxG{l>{Gm)KkP1^p	8t|5guj5<Q,CKBG Iq3}x?d2t?]ǺE.?0,23tSeV*G_#G-vR6?hA<rp~`|+j/O?0~Go%w5 5 A#A|;nnF?znxvgu-to>pvq8O>ktixpfΩ+_yS>)0{jW "5ݯ_ K?e⿉z>_ssݹׇCeRwfc>4niBѐ\~Y#جOk^<cldQVwk쏙ouK8!mfYXeAY ) D$+x[·
;JL3[~{Ck^!n"GFfU)gM
+YG2ɻiScZsK"*+d ѿ
4&_hבGMnwdo	*~ۤikp;`c$'ճ(rlqb;{u"*ԔQREPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEP^Ckꗚ7k)bz zs_<o':U1|=E(ҜlռabȮp99ԁWq7$Gi&PO~A$>#~͞)|]ukg-CѲ{wCTƒP<pOE-ПաbqT?ݽJ_ۯV
bE.]:㓌w$}}Ui$
rқhvk+jz`cT)inQEQohteKtZ*uM-tgU]ݍtU^t%jJ
<L -S?u<v,Hƪ3k<qO/X;v3 +U7'>kE6Wq۬U:ȸUvLB7lVUD˚ծ>&_j>PyUe=3gRt*NVؓ,>5kKWM^OX<.qyq3\hb,~`Asc8J?UpM?|=^,ې	5]]}ֲM)VR&LU;ImO,Դä励
jw6_m)yGpUX\vtjd6wQowl"9V0A5cy&i'O_Xin1u;Q\w_ϊ ڵSqxh(xe+"} fMS2#ki@%,F8uGmWco61TZ-}/M񎎻Oޥ}^
ּk_x;7Y[Y=zgz_) wƚmnt"*n'<sk8N<Isv>_5
y[}ұkKuoI_Qk P:wiqtѮ$p79qӍsj>ےO: cn\+`mUx3, -Gs	V)u>'|?f۲	dyW~tWQ,ÿin+[Wb+Myaj+ m[}O\}.+R:߱ǯ$k/\++k2 {˿cBra'vH#|L  8W!;i蜏V[ kQ:o3$dXL<?Z,pc!V@!gGu_<gOv=B9!٥	V[rg>CĞ~z`H]Ĳx,>cֽC
ٴG&c\0Ulg#Q]msgq
d|Kx/].Q3GEtqV[
wqxGٹ$AE ɧ1Czfp~ ב^eGx3]կm0SwR rAUϵs֨jQ`M&[
n#Y?;_ំGh+_ZkZ6tF:qϵ{o:7tZʺnR|EI3WU!Xeo+ۦs_Bk-EԮI<YB;[Z8c'3+unԵ1 i4 U"Hf.ypI> 
|A%Qs|sxFfk[N

jQ (г1tlR-m SO_x_^X[QW?|<z\O?3]VOX@K$̫oB54H'>mmq#	 *ov'< I+ǃ@<odnp'v<T2sFֶ&uRRV/OiV1kt R k?mnAY@YAG5l_
Ӱ_
k<&VS$*sjF?[\4bqt~Vϴ/Uf
 `}<yZ~μ㎁v>9x'ZKvm.;FY;l>H^sUi~=Ĵ6	X6L$+7g|&٦'orIgA[4WOl`ԭ# ^3ֳdm]bsV] nf7	~$ٙ+>v Hp
䚹FgZm~jV>d#33n$rkՖ(S{+n	^ oėC2VOlFF0)"W˸\uB:r;=q̰zGS4p?\Pn{v4oڕs~v|Li<El NLe]K`;LTƦiwإ~~:qI$dW ٍ}ah6ܘF/t=>kidsb}#?Myn@9y"{T9Ӳ>ˁv eUMŶoy@}AsxN:}o˂7.= ?\ןZO&轤gVu_[( ?ZjK][m?x3X]CnD92]1r}CYWZoǰ(.*Чf=ٻw|߅x_?SGe$q$su+& z20sZ> L(
6N#n?(qڼGROdѮdxT0~nqE;\9}n;4+B.Hz`pZ ,ֲiNP.(z>uD7l_89%A=q KhlWnʌ@QqN9Q85L]<c#JN1Mc Ws2KKB}::s]otֶsQX#ʣx鏛<jE"̲mg m$u6`f18^.3u,ծ%Ki~g'oN+?Qkb1ki6q~gsہ1>7d.8 gLV4YrF4gteP} LαE3)	^lkpG՗#C=eK;krYL2+u\׎΢$x$W*179Ў=}G_n36.<8@zCo?Sg-ϭ3iO35(?DwڿzBz"/N"0CvJdpqdӧ|h%2Ip&chR2}zp3 IєOe<G
h;G0 sox|+q%I2y=ڼg5ZMy׊8ě|wN359i}Z[_CG^Hɣ@ѐ+w>xrj*o\yMc~sJKiWzmp#.]`czyV^ng}㙤ռ7ܢn\{uѾ"m{ͷ3h_X:q[恘e)> :w7Ki}BŜ&0	Tzp+]}|ZTgmn  -,2Ȥl۲O,0UpW 
O:iǧKNU9t/_^;b=3Qӯ@fX$ۜ!u' #ѬC4֖c)Z0DHH&<MY^xr@M
Oў'oiOS	=:FK%YJt@k8ʕ7&g41T?i/ě/I96b P8 9k[Ꮝ-<F|Dڷdѕ!_& ־{ k=~Ziqow[(m,8\Ђ~>xP=a2l{X|0iQuQr+iC>@/I43J[ܞ0xB.#K!M
Ng8'O)6FY#cl|̎zW W	ESwڞ]U'}M<^OᣖEv:<<~+߭w99~?ᲆ=w ޹%ӯvS/!b6$|f<+z~$0H&{3޲VqWF_/#<DoT"oǃBѪ|5_t5oڷ"*> 9< _>6x6xCmd"[B
vr/~xȿoSᯀ,hz|5⯶zeqiτ$F7
FӖ"7.GǡOzu%z?3˴֟5}*M*8#$a(}k3gR8𭴄Ki&( =N9;
qk<Q&q
>OAm̶~yAF
W &]; jgh w½Mo~x[ybܜtxwuR1cWϟ<uΘ8*_88ݟƽKh#|@]cUUq-\;+0FXA?C `7<
knzh/t `;GBcׯ A|A,ķ1k]t`m0qKǟl7ZLR iW;>
L#95xk_-baMff` y}OnzS}_T?hmY fh$߿[2rk{z~ vi.oL! z@k~?;tXXfOwĀ889?W:~
>Em"\LOF
y 	_=L.ۺ> M_ɤƚ%̱3tR[9
	'<x#9iDf dSP񿋵KoV4$C8\(D=[
3f#  o~(M<aaoy:,nXJ6Yl,b敕L\Nk\g{O/ZѮa4NYfyr4'oNAa_xj%ON*1Fӯ}{+ZC*7nq+g;|*MÍ↗$Х⻨dY 6q2v ӎ2P/-ZZNĳ{J׵;˸JQBCAl|Iq^iM*ةjBȱ5kiߋ+ǡj_gJ#nmqU|dc8ϨX 	>$XӣP}*ڤh4ߋ5%3]Z$>AE'hg88~~oǿ35{FH@nֽƾ?ox|<ּGuZEc{emN~hs9n`W7miL7<3[8{ r
$q3޺)x#)E:h'~>,vSkMz]"5͠pX=SHgiז\g >Cjfs)?1}6p{zWu~0bL}.e\׆|} 镒ݝ6Y~1x7ټEZ;+Y.	aT
V|A:X
kIy%}.+
# F1i7,ʴ npT`<_>( õwGao0#<UT+Rά~h|N|;&x^Ya[xdo_zWw  |ek}Me6;\# $©i	 Q_&__U_/I%H=_¼	8|H^ƙCk{'I"K7>OUaz`PT&K\/0gć
 Ή\< _zOY5C;m` AWbtt?ZN.tg3R(320,oP P
o; WX~ ~ucNl>3 _gᏆ:}I߸2ȇ 8#2M W_g|w~ l~fF`r69;ͭMNOcG
H/t|?[&Ϸ6*:  Pqc^Rm	" g<l\\澸?l_ 	>#VSt6,m *28ۜ x{˛_vp5fh}dt+e=20	'IicB]lz>;k<kuꗎJdI5?PxxJd=mP+ov~lWeQKL&.ᘇkS=7LѾ7FMC\Q0E	b gc5"-MR֟q詪CZ/\QE Q( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (Ηow$omc
jASQ@Q@6i=vNO/٣jg%2gcěM%ݦW;?̣qT76@O]۬YI .qMsjwCIόګ72 Q
᧎c떷PYWZ-Ty!?ӵx/jn&m"8< eωt a\}(-y- p]#w+rտj >-RMx<'"4NT*9`=o"bEoQ?g?
+L$, *G{ρ>$7RbAp
oFK'snͿX; #\3[+.+SϋI6H 2\ީEYUmP ) ٳ٥5<ƿ 8׎{j5뵙UR#* uoZ񶩬,7Kgis4l.g`q^}жKT9Hy;v(.6V5en5ay)f؛ʪJymj%U\T[J"#ueO5 	?W7	ffx]o(dGMA)vב暦?x r+>t2:q2k 񾧼I`Ig_߱5ۗӴ[pj;i>hc?~+y~%sq jSoU	W V/jۿo
*ؚz6/V9 o`|>=$Ϧ.{+5oi- i Z9s]XXݘ%h^:?XR\hy爿
~<(^Q$ mJݘ0h!  /xK<_Y$_b>Gatʺ=I?LW[M;&U?~Nҭl&n4n
2f-t?sG#Q}Iγ fQ  q~-%%ҫH^9|o<ّTG̘;Vwg%I-=B?LctП¼T\hv{[H&S5xKU٬޳$M	Gh^Bsw+ h]L_|K-ZEe~yOgrb*)&͏ۓ>9#{dr$2aJC#8zٓNzl5MeRI6` +8!q
1G<x5Wj=$1f4Cc]tg.cM69/	Y*u #Kks1x6pI7O_xmmc%`<8zW~5?eti[mJ+=e]`v8^
oكĞkCO}:	~owa-vxQ( r¦Ѻ~:mM5U]|(vKf
.z ;ׇsqj^Vsku!wln}:ע[x_\7Pe_ZQsJ{UQw=wO;koz}»Ecm
g3L}ugXH5i'<Rp찞4Ta<\cǿ
x3jЪ2_$fl0S8VI{םl \÷: 5C|1eS}H?3c5\eO)Qˠ:M}&2I&8(Wz5C<eCm`xԏκOEnt4V]0ڌ6 rJ >^<{ km/OHf#m$12"ٷŶ#Vp,AOQJ}F	|=׼/G;k^NWd!Aһj	m.^I5Ϳ\QyQYTW^I+Te(QknFy-" O%Gykykf6A,E?)5'ςz A-~٪x{{;Ѭm6}*1B$`%pBL_a9xgS"];-$n q## u1q$7{zݠhr1$=r8^?|}æW5Nrn9Ɋ̓_$䅯.=pY#Sڷw 6WUs}kVmwDr5hs[hkhEotC^H<K(?=TY560㧊Ғ7m'c~5Mϯ٭./ZTHf y۞k,!\iŜ(Xj-{| LY=%6+Y(_4y#b:׫3	 =HH55&dl
FT\NNmoOYn&U
V,'2:kς?WF8}?N{{`;1-wh7_pwudP;$Bp>`'pD<fgڮD'=
sB-ԃ.:#|{.x{I[	hvC-. ^0,$֣\	lה~%?f}CLF'u|g<uٶ+}ޤtק*n:q\Ư4?of<j939=j\q׀zq˚u*5w BBGO⾡ memNH
8ϨIܙھٝ|0N2qq^o,d$TA8N0<w=}M/S-GrϑjTz䃊/W\-!,JFHpw
HpFy{YatE=;aAqEK}>KKFʨۇCm9}Nzcxh<ˆUE@ნt\ǀ $m
'dyqJwo#$q:K-s[GP0c7c^r̲xE 
8Ul`@$uei&EVhg
t%b9=Fk_Vzr'nY  #ZլϜ<Iܑm<#ly@, Dx<|:t4nuea <9)ۂv	|</*̡#69.Tx/]9n4*e|H
#y;xQFxQ^gl!9=00X:e6JX8 0On^i	,꛶7s}6m%ʹy~@zYD+0|+v!²`g<5hukM7iy+?1Tp2U:^WrA#-cpP𻤎O`qצzw`i׏,ڔ~h|m+iv>pϥ_$.#^<x`FF+íZšxin&.F y 
E.JO+kvu
NթO/:ꑸ>c2Rsn^3Lc|aif=.qJnՕP8&tn.3' ϵz6O	93+
|8Եfkc/I,?>"]7|fa}I[-0GŖٕm?ӌ$\f|T4;F)'i?WY̒j#N}(9IsYnv.	 W⦭]]I>#i~Qn#"0A=AS5F5+iH!C#O4Qc̟ *
PO=ǆ$56L\GupXM
,{ݷj
ke1U\;RxV2ׯ׆]@RܬVʞCF|i閚=lZ}%.;3BSPyڅ6+CI
A1rw@lQ*R#rmu+}~K;7HAżpᙏ
* z<֟~
V
KQvs-	{bC  aY!|P2mT]ḳwv#}pHaHx?	t~9{eFloZ6;Gw7 L\wQX|dVRh pT vc--s揆߅\7;Z6x۝Q׌$b	_?_noxBW;ObHZ3/-)~K)>nYt\9uQi
l4Vmf`I}iU£iG:RY/Z|VO+[d2yz?޷>*x;kfKW__?&PP߼*#0F *qϡ.KXZ38B Ԏbʿxt}}<Rbԑ̶4f97"0aW=9||UK-:Z,*) 1Wŭ/:M犬^KDe0C#ooFycCaXne.i2mܬ('W/֣Fu˕OC/g,HKE@. mV׃~~"8mGVO˲)uHVlNy"#?ƹ'5ht""$FPHbm\v3$ץxm{N~-B!+մ쪨ӕPq_;[ཤ^B'x fῂtOt8Q[ &
c4ZU7iq_Kk=xO?Óe<71kYv6ÁH $g_(m|WxMl.;y7rF@'p?{P9&j^OgFXv%f
#xKKZM\#7/,u5ľTlІ}T7K#]Ls>b3
*69hUjH
O?W:Ω[jz,6h2T 3o#xZ_Bf5PV'	>دh/_-4q%I,r6$x<vj?.UoM\s!g0>X|5ڥҍ9k(ƜUDzχ>O
WC%
8H Y-w&0F$Ps-<<G ߔ99s^_կ.ueoKr}J!$RI@<3r8jZ-ftF ʆ]F^3!hrO<`^dMh:rIf8zGJiڧHnټIdNF	#zsv+ ]hqysc%ŊHMӌșclQ/Z]kV״&i.'g0*,@c.s?֝ϊ.<=ju\uЉ|,X.쯖é
kRSz]6<Ya*~<n<6چ5k!&9C_3x_˫xta&3.ȇaQ)99"&K_<?ھ$մ6FRr<Wic&]]p;HӿjcV֩
0B.1\i:SZvz{éٷ|8.,Sh
|f fp].}0HF, s}XgP-dt;Lb#*20*qZQ״_iM7ԇX>9aο1a^*TmGRQ_}3xVҴJDpU(88=+xG/3x~k >
[O7H6Ol՟@=,Z	,ê r,G/OپyyhwQ jM9JܥN1
8V:CGZ:ևpwi|N216dQO־ͧxg2>b@(<0k^;k~kKn3l2Sc9 txS MPOo6G{]wO(TvA;zNJR	|qG8~",%0(朓Lm=G>gkxJ[m685&#VF
y G?hϸ?}SPΡ
.e4iguQR7}N$y_TsObt?"[kc~4b7Z 5io+w)|]t=/u?
@w/_AM/6s4z69~nTk4%ʛR\s )
CįuZ}Qբb]A ?|Op|R7uy̵_\HS 1dcإLOtcñ LWm(
%?;j:n{φƙn{ӨW'?W˞G?_Dk3A ң|*kS`6u;7z+ ďO25tFP? J۷\[Q~e J1ɖ,p?~W=rݝ$Vygÿڵ6,	#GlK}s"Pr fqD{N\y~.q#H[St*SRb&Nm>hi7፡iHO܂WC:}òk>(Vq1#&Q0> a9fRkq^^>5I&4?PYb4I;n;aZJi <I㯀׉8o4_kDI(1e>ecmh:|=k'-Ě{fPn#P1+BbNy95 D~մ4S	،	k+Q%k+HBsK :?EMYZi8綘łidFنUA
A澮[H^(j#%%tdrih(((((((((((((((((((((((((((((((((((((((((((((((((((g *+u4 $uV®OSk*w5~uc-6uS*_7axT YUm;Cg C.39*:	眑=:
5n7m$v 
E8)Wy+ ۯbu%>UIǬR+rV
[̪pv3 r;>$m]\,,F䓰~e5mR~}xW*:G%"^%P<;O@dpF}]g۾f 1^*$\'kyumO|K	7."c^O +uf-;qǅZIoNd-qǎn.~+6c4dqӜbo}_m@٭O0I_q bk|ckKeUc%_vVSW?/?o #MK¾[mR;φt6Vm3FVr|PTrŇ I=aoGSԌ^(bG# }A߷񷉾 o
ͮ1	TH{ps{_Í_^"յK{+mKtj]xw*e e9i>?sCk}iVfhn>!j&G?,ˏ+$th5_p)WrhB@@d﷞MrtɨXZsZ^·k\ޟO|44+kk}6MӓF+1lvH׸
zbj;ev>QǨ&VH85@~Ouo&WѿoxO}7S|[Jsۇ+f^ ~O*Nҳ47<OFѪK+WN ٮGoo0➛yjH?dn- *zp80U@BInݦi5Ok66OmiI"F3VbI&m?h-JkSjFsugo-ݠ(1'Xl)/?8cnO_6ߍ6vVmv| U5sm9㌟V
*Y<zkÅ z:32$k7OS=ƽ׊Hۈ$ *#/B1m6?;Yy{cy 5rm Zs
au*]S ug&_xz""6Qcd#͈S>c
zQ[g&*\=зu&V̾[})kv5 >YjZ~_XvpL"
$}m_X5qS-	~<ps| dԬ&kNn.>t$	JQ	8]KF6&׶څwEc6Seԕpm#2c
`*@+[o7^wڙZ\d[$yr;Qj|U5g26%ͼeD0H$T9<G$eR<R7 kK;]uC
źZt`1!ka[,V#T~Gֽź<$tE}׿xON᦭ŭ{AvDIy׷*je pRcux#;x*Fap9>VMޛT 09e8\Nu0mm&ws.۲9u#N{}OM`t @5oL;░kyu]}m#VRUA
r܁;+֭y_^g%Z[<je`UK0
;ZK	
F#߆ >5
x3]t .V9dIvS&0svZri5[dHT)$.@!kK t?^t
NO e6*Wsg'?׶~%nMƑjݶgS"fS=r<[}b)+| Ix!M$ZF7eAָ
O?޷!
 E`'+о,i]XuavړZYKm$<*1e9
d\)}#g%q8^}LT!R-imXYW 6apv룋Ggt?5TX)<d⼧WצW5 +%,XT푎3&ť7|FW9ula'sw	1[~_[kWlEosCL"X?ozTݿ3^ɻf	H^|% s2Z},_R{pqW| |NaS嵭M~l$#R?>uͫkΖmF0>.Oq^d0V?9x9nou#\4iˬMnBx .LE
]c-P6N@끥l8sӣˡx{Nf+;hm5v;x1HT׭eխ cY.~&1VPI IG⨦uGHvڂHJO]=[o7>*]W~˧ Z
,צLq*2WFf:\n~"g1En#q;W|? R-=u[=;=9uxmLpU6+|;I~̚x70wnmQau29߃K+?^ύ>x[genaMN֙:Cd)Go/(CC
SBpw~*xv.k6p2+#fÖc?d]XKZDTob !eFFYdud?uu44k$(6Ics϶k/&
CFo{$[^ш+3Y He+`F0ظ)'# =?mouյf(.,,λ\h%FO>Mu6ok#}@) *Uzm'9ßNORO\.kO$S*EhJ__g
@0'q^N"N
5ZyV=EԤmaR49<0qڳt̥rT8C=6Piت:Um,KY'

r
߁Ⳇ3-qz5M*p˸Jbc$6Nx MGh؅Mdۻ˞9W>%U̍&n 1Nprx;{SD0̫dȔ Ƙ;cc*6}>QsB,3ϴ %"F
?7I=I"	!H</m;vcHɍdeWq'?$KpD1lRA Y*X7mR,-byh6eT dxw<q⯋Vq$n׉N	8 V㌁y Z)KƖVL2*t>^S+|kH-i|?\Ү_-9n>oz0q]<DHt{Ky\aDEgz-וxZܙ̯BrFy`AnOpcO!
$'
@`8[TZbYFð `G?K8ZDM٣McĺagLrMp?ێ͜nڽ+|[ڳy07+|7nܑ |Zn:<l=Cd`ֳm8\31\&Sqhی
gf"3g_X]Vf c~\fknh͖U$CrïT!ss㌌`ŹYL1FӞ95%Ϡ<MJ鰉n`pϴ,9ּߴdVֱ>A^_k`Mnalò|@񮙥#HOOI
p3.J.wږ7f}1_ᆏ6CuTt4oٜmXc$ghRG[I[jk*4Y,W8΋HF gXsp!ڹg({V߆h'Z[yI 8_c**U]ir5>MB\3!GBjYJ]>@<n<)x<2á1dS +_S|zVw
_d͸}egvOq\??g/4\7dd-$h@
q%|bN~m-|ׯDΏqrKUb5pȧvݞdW?ZjOY-) ##qTz}7Uۭ'vYV3Fz	ey<&@iXAoݧo-W$c8
sJ}B1QJK=7 7 W]y~-jrO,[UA νS<MQxVi|WScrq=
{9#[*je%A]'@?<sʁz?U|n euu}ZI#~r+) :̷1#
:9aGǽ_U/GkۭRh7HȁqZD^9 XU>˕#$pGҿO eؾOpڵ5hNyq]}ɰ1)<zG am'mooO届+hfAA
.b0p8RH5z0{1oG~J|.IƖ:z޹0[{AĀz) xZh<}-#E&Uv + @-5;.~~
"cf*rfKaaFxQ]ύ$RWkms~LizUq\?7A GSO}RZӼ['t:dt&?cx{ᦗk	ao3jzhqo,1|PxYZ?kĶ:w;VԬnQbz2]nr;0C7QzVk٣hU2rw1's§ѼMuhY[kDe5VnJ$y\lŋ}}+JO>s+i%eAmDsm9ck$Ԓ@2b]D}K9G|cZGaVNeV>XTVw<08H
v e/C_Kы-'M:/3$1`ʡ!gqGMuo.!kN' e)#~57;[	Ha>e aqFaСIԭ;WdUex_ƟsQti[Ze6<ɢ+0cIp:7_h?ir\Gj1aO<JSݷm8@0~9!oV)743QH\$ %BdgtQM޵$>kHMݍ8TrW'3JcȒխ[
6~#Ҿ-6b]7BBw|ћ}o w=<[ƟnntѢ4V7rf I|+8)7U $/g6ҾB2* #sq '94R.yZB k8U (#$'ve۴M^$kcs}H
!ei`wc*y?ä۵{{{X"쪞dp{Q$@UV`3=s||?8%`Zo;yd4ads,YAq$7:qǫV2o񅍃`;|͞WEY<7<zuX-.=^uKhK[tXRp2>'&?趰Mv%لB Y<.*Fھc}oa,Hw*-d$A&3BqsẔy$2m62@8']*)la)V2L=A啚̴ʹ8{FmS`+KN+IEP睬WI=klw,Ø<|qA.z
6Gx$[1L2VG+;Wqf.[fx޵Ƶq|PYGk(c&PTguSFqwMymy
m8q<A
xoxgUUaV	 sJσPcMS~MGNkH5[t-r(WVRуAԊF} k-ׯAkDItfnxՆP{ pxKH l{H;GOs_Q+]/iM~_ͤjD(iT1!qzJlj_zt4tou!hũ:r>E(GfzG_EoqlH,FA?k2?]O4»vrq"?O~}ۣ_1X1eZB#mǥ}x[&֮U<4Wi5}Z*qJ/f|?~>mEj
ZLE^;ۤ>{Y8+ CZ¿?-'X=bmq[fǀD`v<OcB4cP.m.捅ģu!{%ao>WԦ,-FI,Oλ)+rSԧR;o\i r?Mϊkxc+4xEcVAo<dmW9NJj
<o>YfsN$V9ӳ5l/6n8G.#{ŋw᜛ ډ#1sW'=}[R[$ό	k
3n u$9+g
3~,?;?/S[#ZǃUFmgu	#;d~nH뷿_]1Z6$lS uME2		ՎΧ;v<׺~wqj>3 
ƺs~^!w}Hp`s׼:5MS(b1Ǉ~w*C0/׭AO̧bjy *߁ڏټQqEkjŤ3\[<[řRO*\%$yGmS[T%c=BZk_ET4A*B7d33>.?EO-մB8Lhǥ9$мH&`eI]ZbL4ᦍ+x݁W ^_|[5<jɧkpWyv_;oiz>bC$%Er`1^FuHdTy`X۴H{h5'4zώ$K֮ML"bpCyEFwad4Mi]Ob8ZY 1;0fF>s孾#g]A/=RATvnW.Wk
Iv|!ɡGkqo$m`В$;pA3\qhy?N?b_A=wEIz
<*b<Bdrwg'HÑyz5r__H;SW|}jWƭ;ݷTˈg
H<s_ \zΑnw Zjk8MN	r(@( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( &x?$S R 9r81_)׭1/鶻|?kX]LH$$WeK{oۘ|&BwknOb35#]=+Rem+-P*Kdg
A$|y}VQ^pXu4ܑm}:ƗGHԵB+v7%Au7Ψ7
N8~ן𺴭ZVi7rJyQcTύ x;9ϴuW* h	e-h?έ˨hI0ɧX@33;!z'@y3$;het}Y˵̱ <<WMj>d[e⡁(ART_% x_I.#>tVcV*#|'N 88ffitsFdie[y$S+sn(o{ _NNCKYaZ:JJI$c߷ώS7e-[,b+]W s+$v6w&T3;m
7}8'oötYR!vUmr2'_?v*:i.ۚ\{7I1BM[w@;Z&;H<N1J|jGqo!3!+ ~|~xsZ=[M+~>I<ep98j|WS]mMjLⷎEKh&L7}X]7^][[h<576:^zO7m=8'8}qHT]6p&k[O^6բA#
̻Vbs.p+sxzW!c%LJ(r3r:Wh9nR+~/V_H[:
=N+ȼ)=1f]2Zb_ݴ,LAʼH`܆
3=?hmZveXϩy1̓$Vg?3g _*,ռ_w>]KQVӬuhR;7~gERb&Z.|}<%{.ʬzb_yAoj%]䑸ɓ
x?w%[{;{8&i,K}"+4y9@f	#ڧ࿊a[M]?Vխ'OXbG݂Θ2n^=|]qWZ-r~sM/ʋ'X ,<\FsRkV|Vl(|VuMkI6=U+HJ4AX2F]&NUf
4c"ȕ_ <q{?#^i<#Ru,r
  D;?Z|w>>ҵ+;vELHrrJal-*SRKMwLjm%4|>~pV6Cvϗ^|d|' Ο{5$j1"ɸޖ#z'5G=K^#?k'.a139Cu)=reŃIgm/Kdg=:sm2E3Ƀyl *b #|-<njbq3|E;%54)(_2G~#ox:
}sqDhP-U`Fpk돇t?Ps}uDmw>x_5eOsêMmmi{;<$.y<ݒctz7= Io)F_}xrkO.;l3c.>*U8z'K	-FYZk!['?h~{y,YSk{r=x_^ z?!fxw0lc'U_L>+]UcY?$m
lK`Ў"o/+YRHs {>]7|o&kk}4ɔsG8;b6r5zblncXVHI©*wck pOZ?	|9a;_2'v	0hULh@K
I{Ϫ9>ey/G&jV]#5R*N1\gql?q|7|A_k:--ޑKq>4ndQLVABq?e?V/A4!ҮQcA^]%sI*xS>qy+yn!<20$Wþ[cr|o[w=I
IpچRtym7PW,e
OCTo^ VPV#2>T$
d#<}MxKM񞝮BjZ"lg\l(w,NB.jo	|1llm]./('+U<qGhQ9 Jy{.LpN[֖\^^\Z۽|rP6?ċቭ4{m̵͓+T
?Ϧ{oGZLןjF
uC,A$?'27rMgz7kH0C9$	ʨ+9	ӆM,<
//{;yFzs	x s|c+y{v;
>dqЊQxÚ-ַW u#lRT'py _gj_J~ZV.
n$(  f9ݻ9tL{浼VѤZ>"ғ	$,vA8{KxV~kI72͏4"H/qןdjrhZ[KrҨ+G0+.bFk6fQX՗g'65#2x4멝<4jGCtKR45C,Vq"O@`951#C3"r$}?[Q%7۠wdV;H P<|9_:𭈷;;y&x_nb*+c\g &3~46Ɣr->j־,J5Ԛ o5QAvP3ioYm"o-V,)R#8A=Ƿ1xG;xo##(\@\#$ڼ}슞4[_ZYZϩDKjy9UUdJNsҼIqZwG)gY-q
wO
=I;l6xUkZŽVrJMd
YAd< uy{Bee1, 9
-y_ Twt=/Jk|e0fT ~CgpeĒzدM^9+}.koHOlCJ(*f߈?I&kqni
([v#I|JbPϭ{'xX%rARFf]A Ce@mxXvM3z*|8 ש%
Qb[RG1n؞^ Ȭw3D9M\a;XwqYctVKyбɯ,|'>kˣq&T41mRO$)ك}B.!?CHMt;DyyԊxJOǋZ~mas"6jb?s q_G~Ͽ gfOҼ=;aLO3)
 vXwM*\KI.%kU[I(NdQRT1z7AGnp]S0HG;|*s暽S,׮<i>bMLm]	X%`	vMeG!a{Ytwˁشm"L'ry`kC [wCm$.dETdL!6v<'
|Z_I彷y4WdvHdP0sa~Ic*09#GH"\
:MhK$>8Yc o+ ,1{WOkǞ%߃Ԭݔޛq3[He`l# *<p% "ik'6H8	1seX+C `J'rf0c&O,&YoT7 	
pn'8'k?d ;anfH}G0Ty_i/y7%mg,)6SrCW	oi>eH$YF!p-R<0*].z8Z|Kyn?slDBd(sy[ڋOw{:y\짻)^[=>6mƄ\4sBYbnz0 $d/cJ=7Z}].[{e԰C2rxRYAMgQ_O_MXL4*_
.E$c<VVօ0*>HI-&@-tCo\I%ͫUylbF{99tsCuyg"۰6$1<<uG0s]{9c"nlh'HA2+. %W!A$8mb7(a;`	bTc+s /k0-͋yh9gpr[XqfGh:/r<YK9ㄈ{]XZjTTݙO0Uu?o2p vr*@u!H 9BiZfDWzeo0-䁞}~/k^ݟW[umا

KK>Seÿٟ l|;A5f7.HJY؎ga-XZ=c[[g1	 6UddN2qyqےy^^]MOψutnya`f=IrbI<ßo$lZOG-ycu&tƛc*GA̪vrΊ{̺qsGqLy?-Fw	˸<8&GR^=<SIX2I#fEP7k9
ȒVn灚*PO#5^啤ܡ A!=ky!0!uH>_^AzNvk&fO;@m
 $@+Ѷ=:jDR\~IGdyvap^L5t0)oC?d
gW~)E->O.ɆOz^ǺφWIյ=V?j7j`mE)P&ʻF:W>>=휗:˵Ϛ=2w($:sԽ%	khV0MWQMR8-ʏpw䢃rG&Wo_nr<'6Sڡ73bdF	mqܤ׫#gM7GWY@0K̘*=2~gYZ>Gb{y'Z>rÿgͥ?3<*5"xi$LA M)UVkOc|9UXK5ɮص:6'kbi(Dklo5{]Rm6fYtŖ
UwJ08CMƎu:7=͌:^vg0طjy0[zLt}mlFw7`Ay.fs	F+
z<Mkyga#SQtPv(-|$ڿHOٓǚCciw=2pVѠ/,b$Հ=sO|^t;*#fo0}sM=j&~b*0s_xőx(P 흗$> }5㟊~YˈLy
@'ׂc+۵+]B=!Ĳy|s6q@b-ȖԿ2e^
qgK㇆!= ýRHOUNxw1L9xRQRԴ+˫ '6IhʟH??a *5Ysׂ<YGf8i[j-=0EW/Z]<lesGT}yO)
v7Z}
+1;@}ZkZM
!4	;D	_/4Էc#0̤`
wwws6I$8'Tx'Jk6mv<ڤQ[ǱҵlVԊ?N;A$G$lQFAGtVR@|Y_=?g_Z,r5In[.X]]X~D}	ص]#V;[yf-( >3Ҿh4~"Kg%rKH6/ks3Ѿ!_kKw61yvc/C!2&5쮎2\]+Jj=~s
fX^kZIgy>߷ޝNVUm_"8
|Wu{Fڱ8tv0h?)Is^Y&ojSFvy+F_ݝGGtxJ[;A#<șϙmFk'.'k+[/$:8=:ףx]|2jI:3*$$p9zl|u.KaP浖8Mj,["PI+J0ZjyVrqVG>+5$|ĉ|t_+*0nan|=#WOx]&ul'mHj/l#La#
e6Km	u;M6յ$&Դ,q FGixQl4Y#K!+mGo$pK/rH8C{v
e9ny?]j[m?hh66||'@GE }CE,a敝vbTvCa[-_^j>ҮK'K0sbK72N
?PVRhxG
u$-JN7I-BƱb;G6qwG߳φxZ dϻ?fFQy̶)yiH𤅘 9灸pp >(
{^m~%Dq:vW#5'G6$$;`0W;ry=G<
l4֧J6s<h
"InMI\p e藖,zEqs%0A"ȑ>p0G38ǌ+~A˛k+[uaym%̶b6c'v~cxo gHGpN>\`N8RA67g&+J6zs좹-1elG9zx8\ m5lveX@9R\|0cot$-s2#${@8|2<?{-eI" qQ^ʼ2X2Nǵ~_5']KPvg!TI1c'폣|)T]>SYΥE9^RRI#O<?<7m%i"Ѽ(QGm%ɻ<\F|q[^˹ȕ_0+T:@ KZn;ևҟ7xUKLwQ''9Y!W'kڲמ9Ƿ%
BO3\xm##9psEܪa$iO\0F2qku٦}i]j-p2k#suzg =3u)^IjQ.>&cC!ˀ< 	5N
8[?#RUPdz?
}.[WTԾl\?񟔖

:%');Wxċ{gėafKvXU%|q||g}	AUZ2I%C@s0=O燭1I$^4lfU?tƾ	hZ5*^=i参~}u Z/Omkn<cqcli)KȪ~-'Fk;Hl#$xfT9Η-Ns7xw6cFd{\G3+ɏPrX>a5z%ng($x]gO~k[sh-jm帘x9#i8Q>k^Kr> ZѴ'oʣ~[h䐪Ll1ӯ|UkWZ<]JoH>cp;~Q*zQQW-EKkn.bg #}_,:k$ws
>8|=G:Bs![o=Nqҹ?k{%vyrN1zc(GݳgѾ|C/.z{%帓iےTcn+;~
xK}(y_trF@]+A5@DͣM#>NyY_XoyM&1>wMb#hv6j1Pb<˛=V7$VFq$rX*L=+Ǭ55ȱ܆mHU"h~&1ri
d=xȻtrk_/tmxznZ$#<1c\# υWs=,*Oz1 s_>
n]I6]A"_wײxςu+Ū"ea 1ETq==EY_?j|{.7sEn"DyЊBBȪ:v \v^֙GIb8"1g
,܌d׫?Q'O-hR/G0t;^O*8&#QZHI\R
qE|~/mgUԴTA>bJj`A[z:Eh0( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( _4߆~յY^;KU\fG?ENyݷ̔=6
QӦ捰Ex?m5\ZGn(M8#dDX% 
5:}a/ZO8D=x #4#p$cmdIuuh!`kZ
Gկᮃ,KeZyg]EI/TD<v GTHXx܋v9 ػmwej[m:g-w| w+pkE,~i;]rX-nGF\I'>wqtN{$;(5.U m x{[j>t;]k_heXe3
1Q$N<| >hھ#xgT^O.G{6IAw`1YoaRNn<)]]2lN98'4__N?Zw֚l7QzEGɍG3 K:ܙ͗'F
E	^>#!]T}	wS?c~$WxSki/+bl@aш$0
Is5 -7EZS
0HATg87_S?hT>qoo+'a[
BCzc|"\**|#E*5m_IڏtK	ciw|B{❽g2m~qb-,6&5fH-$_sx0[xPPu&tRPYzs_&_,|go5ǅb\[)-|Fzu澗*rjJ%k4~v~;?jf6ԡi*E4D;MM>RGcګkgbLV8v^3x6Xk&F>TNݫ??Ww5mAċ,/hgpÆ~{8EƅEn}G?Bm3Gm+9"8tn2 ="|!w7:x]Dsk2pyE<\_bxw	⍶6oCmRQ/<7lVlg?{9C "}|CeiAg;+xr-
ԐE|ܸo6gDy;gzwn4@\G
v̲<)RrF1ZO HldU=~b@7u<^"OGۥI4ۛy.#8UciEr& Moӧ|$lמKrHs-_A
yZSm3[7/nkAdta|`m$s>|Q[kuk]vjŶG#!Ivv
ښ
CN>Pԏ2ix"sTԅ88'ZƟHqgUܴO"KdaGR2'?pZSj)/Tgf}Io	U(G:-3r4EA <cxXǇN_,#0%!\cb3[Y.A?ڴh Alʝ̌~\3LmWr[Yq
onHV3]-A9jkߋMvm~	k0CIj]TGZ=,io ^ᯅo6r-Ȓ\l6q!׉$У..4Շ/Z%8Yw!Or+5X3^Onۧ0*ˑ8$彊٥HÚ1n4ob+_kuŭǪZƖ vtb9G
rN
*HȤ̋PUX4Srڶo|
|D^fR-_긭+]"SY// 5OI#PUyXnn<'<C}{Z%#5bZn';j
udp _T? fZ4Uufh-o($)R|ƈ)%lzw^m)rͩpY>m8m@ M:5]G(	*GbrX⾣j>ѩy]N<E%xI| |MqOc|"_%$Aܪ_g~<^xNhft$;{{1dS'9-`X1Eo(!ԵѨX[BȪB"ؘ*CFT$ψS]'6qcjb8g$+4qHgBW/$dޡrI^sGGj&)&4.5'j:vr2L*C!a.2C?j:Y\i e˒6CH0roi@2!CN9'fJG?.H?u_^\qhɨ\vf(!T685bxY>3oc#wzngMvSd͵O$l;;T[{=CQ!9ǘHj{?xvm+MMہcv%*aLvp@q !Cφ?c8n%'˦I#ʀcs݌|_OW
IJ	] Kh kR%f`6	$hl|to
'1¸#td ;5xZI)4$qN[|k؞>)Zh,m'ŋ͔H=o+=\5GWZ3MƦ]Xxk\[m`Qo.I,mQW+㟊ury:\nlyƏ{ Y!_7л,q}D(Җ,O>Uv:?
WKkBAj cps^-iC/MV;l7 8
ʡXr`u|Vﴪmxyh6gkx-b-׶R##ھw|=dk_їR*z<xF\6KXB3X7?uK}2+ށlpF߯&NՖM@Z	?#(7d?0 `Wۺ-"=:ɾ[ۉbF <qTpJ_M&<Wzoq#j^L%Gˉ0xJQ
Z¨7/C,r|
)UWWvю
zGmj4qݴ3gi ۸=pAɮtyVW4?,CgRɪ-LE֗xwpZw #OiV<BI۞$wO
ǚz\6Z}P<1#ĥ8,|3kyḼդ{cvKyd`
/ %¿oˍi@[kf#|v
<eXG
xlXyF.<?6֛$ ,/z/~#h8
nidӡQ.ՔyS/-נoR8099.xxð%2F.O=0psTm|IgE
۲7mШێ:7?S^b!MJwseo&$sG$( xsp*]#³ZC$Z8BModmC>f X^$Riˈ!2Ļ1pIڤcnXr~L_C*E*"g<n@??^%RQb_z\XPy5RJwKsOk^ 	-cY"ܡq|
1%PԼmO6sne
+$vܪ=&k?6Yc  ͉VHꭴqБ_0*:UR=ϮOڛ̾fc^[y#5-G׷"%v~(n85~.ͫX3Gea)
lJ2J2U$rAG:UUwIn`@ }>y|FP n2j5
;ξYN4ʐ_x`;)A qyE
Ѥ	-H"d@MtxO8RGF#?!}Of!^(+p'h$F6[8#o
[8uU G?+CFtgWx@&9FF3ч(`Kmc>X=0@vRpNyNk]F֖p,mlܪ;W9|86#Mh#u.	m8'׷#);F,ٜπ|u[;ubsndtw/ҪG.`# $RW0ᘐW]SXRI<#?2rs9QKW7vv鱍[2n< 07.A 
I\ʳ
B<ҫmnV  8q_Zm6yLH4)b*6 `+ci2ir{eܤ`8ە@e
1m\j ]<n<Г''wQ5׵1F2\F^῱juaq\37bg8 1^ȫǠ|EqsFUG[za?`>$Ny_< ISG$%ŝkWץmY&O
yla9pqZ,f>k=2Ln/|ŉY|˖PQl9HeM $w7Kp&,Ω#y<.q/T4ۏHu+;0% r26:<]Z4g
y|LFq~Dp8naEI! 7(pYl6"7Akg,z<!i:<qFu擭9//3fs<Wm-sy$v1nH7>D\́5M[s0VJ>/iQ][ҥ+<P졳0Qm!u\%Xm2]Ȋp?1$u{].Q7hԧKW6\\/҅]υ'czn?[.i2IlbWa$.NX[ `V؜SUMۢn6gYO/ $̕ك;.-[IYmBTEI1D9t\2cJ@eZjm1Km[q##wocYWφѨ-Ҵ}\G,+*`7~sK*ӓM-LjIi#%n~T<Ƨ9y7yuc 1׊7{k/"o&y˴HffANI'>k|k/S9"i6sFi씏pX"ʨo'wM0.&OCڒMbMg;#yz_f𗆭"^?MPr,[=VU=r>/jۖDMw_1vakecd?xğo(_]Zm"RG)g~pkn_ɟ/j3>~4|W)cuq_,j##yqGcw8A$Y'1 ֯
?kz9-1``;N1O*žK!̓\%BɎ˽wo2|ݟE"t GH s6Նع9_Wf;Fkx<ۤs}x)M|D/v6h@.Sv;8{ZcgMkxmf}<z9E5X=T?IN[geeӠW?Xn5toj{%m"O.6$H kj+;wRAésnH-k!]Lr{te$⿈>)&5MK){	rSI.@?uO95P5;k/[ה2I,c`JN;n&R>:M4b*,_7}SgRӹ9PGW_'z	o|sf<"Ȃ=#0pv+3V,֮m:EP;~9=K?n&4xd^h2d9\t8#_9ͩP4NәgˢWFmJkCHAf;`  +""cn^Zh%߼f݂rpxek
χ-ЎuY?<cx-rV3SUf'w_\OozY9vT%ֽam+
o(h\ơFu(Rdea0O?
KἾ &-\7*d	.V#(9TsE-&B*Oz)8N⳩5UqW_}f:X[Yݶ'NE_Nnu[+P28<w_AO"Ewit%"Chأ|.O%qQMd
38u⻋ ES2yG?x$+-ѳws8ǐ:zVKiTթB4Zm??PEa[ l{z]	>*-I6V.΄~(}Z-n/3ŗІ+3`b1q3_Zx
c=_H O
D"-Iw+oQHrKqǃQX)=>f#6gb}z-%>Wf82ɐvu^G[_
:'gn煉0I&~|pv7ňM$w_1jM+
(\;I"npF0}J/سXoOSX|Aоݤxbh 8 qM
՗%x\Ƥ) 40 V[oaX,cxI`0=Lx_?m|CiQE+IU[ky/*qʏXKŖ;1 K <妗w
ho|A.k5M{%#sn}k̎_n=:^Fַ"_ .kST̺V.;eXaЃ/]r;nMԬ-k+gV:<I|6"7@Fye6k}cX֯.%T6eUʥ,
	xG焭xt
ͩk֏mqw[bay> Fc}N4҄U]XO< g~FQ_éC$m＞U$u!<x~F5WQF.(v6K.H8c-TS2%
$8B,UG9O4-ok$9ʛF8OZϖmDU/j7E_ڽR[HXe
< rMs_V ?YR@*R$6r1q5w·W̲t[T2˨jRxK\IokŏE5*[vm
nP%G Ms0hk%{_.xv3cm+6vo/$TUBDl wyo[pM47;>,vNAZ2{ѓrkBmw0YI5n{csY>7Pڬk4l~b{zqz8,;ȥ@8P |-Gs8z=5=Kt+ԕ-dդӢFm3]]5ŭ$kF*C1;;`v5K}Ac
d\䜜58,m,ۗ%G8G^'4ӱR^	xx#k%?v޻CgǞp~VfԎG 翩y<aʨV4n~b3zu}[L5joV6 [i\\o;q$fW
$>Eͭ, 1ePpPOU'ּRѼ-ݽ\ ̼#g=OG/x:w?W6+ݦFwF	^3֭Bcs]Y٫I<I0a ]+JMv7:o(ܶ4h@gYq1+RĬKu.>} 5_N:>6Ps"_9&a!חAFJ@~U+{6s(wgʾ&{: C1.8Ȕ?%d[/	(m̤H182:}@#w"{{hP4#KKh}{xfrZͦ@;zI1*?գYFv_L&F۶єFW{qo'ZM8㜺 ' }k' =׋<TȬy8G$cW|yoßxI3y8nTrxOuq{8n򭟌c:.օl)g֠վ#iŵAz N{ gI&Y!EK.e$OqN]wPo]&8^`ګH2#z#zr[ԹS$il+.kg(ӧOκ_[5|]y
X4h}'_I U/ŉ
h~@晣lJogZxGƽ
a@`H;g?z%=W"ݩwAyl͚ EkIZg(>өI}}kHh j|XC\El|sQxOEx^ӿp{sFi>@-rZtߩZ^ cn־#?7Q(dvʹKGcXͿ
5[]"iJ[M+27#:{Wi >u.;aWfw	N$3[|#[?pOg!PDv68BҊ3 fo cxMxPɚm4 !d  'ZqW?%a[kn-%!Q_Ļ;\5eI==uv ÏH d&a*)mYo1C62I~?S/êiz4_"vQ1îW_N;?vevw
GVf!^Lgc׎QR0( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ;Q<-iz~^6<sU?:=>dv[?8X?Ͱ G
?i_|_ӛ\;|I
"`]1$,&6 ؎pܣ/ls]w]KP5W^CNmn#Zl#' X`bOnSJդ[{E|e5?{ܴ]4;] ~!Ǆ~-xgZOKxGYNX$xOz~#~|Ihڧ#yam:&[n1)U ^1 Ikh9#QiI))X~@7  <\xCi6	c8-G)Tw߱R"0.6^|YKPo
t+z,JF=uGĿ>(ܝkCduds[T,޽?|qyVTg^Ax>#MLIh&@t5|wLUI8ɾ|꫏v~C_ōT&Vb><Lڜ{Gwsgken̛J[[ '\x=䍪adŗcsWoG־%W⠧?J^|%^i? 7xF^uBMR&a@Ҿpd3sxO?.ե*_RK裑|[rA ggaRuf
@-cҵ-,E(su|ǃȸZum? W<7j`54Q=d * k?M.GVN4NQe,7,mπOF}MMx3:U=sMֿ}I%|#&g$!>yImK+Px?8,7R[Wkoz 'IYԾO^vV퇌k^$4oZ֥izc}Y %6u^,45~rnS/w`	=sR[uF3[Ex8J0i6?Gy xΆuI[gl"Dx=|xVkXtO bڲJ2@ ze?ۓͱt^|T7'-c_gkG֪w	ӥk ஞ8K~Gq5xhVhv5"u) {oh~_Zn9kKy<7ood&Yp3c8Q~[I
}3[y'`C[~?Y`ji#6&	C k5*?vqLxz7I6Q~!ɼ'i{ЫFKpBWG3U<y!>&s.$l#z>xv+vWk}X7_ ~kxCM[F	XX#:eTcw֧j|PRN<[W?_<i' 6.aj&N"v9'qz³^:u6\>7.
 ھ gZ.lHdn 1 ީQga\ZܥwhCF;OכYԯI]aR儴 }=g frm/$B	qJ1) :i!iwOl^M#,#
n| +|?ċě?Qy,kfFU1}T`k?//|n& 	mI[[\a:,.<槕`a/iY= 3+miw3$71Xx7*7N9Rs|5+?_
|e[VE(eM8;'5\]|>׵ xT𞿩h柩%Ŭ:zU#[<I h)rGlaՍՅĖLŕ̋!fU8^xx	]5+}G^% x
OZ\xB"$B)_aU	||r'⯋ڦ2KcGYXnYXwQЂk#P +o556/ ۄMvS,BO,
i.ſs\ gS}K>tvz73`uHJ(ն6mtٯuLo2IlFR.nPp_,d:VdJn#7JʁÒ>ӿ_x~èi .gGpasrk[>5k GVuY&%#ߘAxHV+59/'~*iWz}vڦnԗO+h XW`|?nUtϷ贩m1o}'%ۂA^1^sWuǆ h/wRj
VHeܞ_	<drȭ++T [ci??:o])#M0+USe
OiM4դyz~2x\l\;,	ݱڲ Y8[huLg6owZC %뷾"2KEB$V* 6 WZ $</{[Xl'aT㐶0ݞ1yCS©н'!m7Iծ<ַ@s`{T	5,
ջ3 !xϦ8o?&0C}d "6Я9UHa s}3GӼ$Zpڢ Uv-' +gը[ 8|"jZ|gii:
y	$30sݼ`s֗w-axω}KedVڠɸ|W
xLx?k+aE?.vR93du]$	W:eg*N>c	qR]oulvqɮ.n>}k)LĶ6>3QdψMd-kL;2ܻQc=+X+P̚]HҘTabI8ϯJsZuBgfc7,'wgqhb)ixDox~壿o-ccy_D8p@!Ͽuq itMog39e*l܎ +g
L=6k戻]YS|RE>cz/e^	LF	qrws܃^U>_J?Coi'+_Qx\]9i"eX3>r~U0'ںK7R_$ߘepR?>98"])^UZ9tIH*	> 7g?&پ
މ͑.:79FuU>8n~Ti_5->mwk	h	b|`\ِ j4;.$#fF*9<}pycCDُb[h'mHai? 
D,|KCFȠk]97:Jf%_7~\226V!vp}	&5?i9Βy ʒ/NGH8mWCtK{ⷊ4/"8Cr@O8$? O=~}BȑAu{ r0A8ǝ.
:1xo]uI|P>e9'YgoZG}{f[MC#,	:
{=㗅x]m̖)?71<S |55-K/.ku0 xxwp Λ~2{;MsI{]oˆr$1.7*v<cy]o?սZImf7c*rĮ#p	ǃ4_[k *[$H_;9zְ~>x6&/4+yų"`ERH<`g~_Ζ"2[ZhD}?ֺm
Ŕ:4&ZKR  $1]ŉ3Ꮐrk_(4ۨJ4)%.`06Iq_|Fxڅ6e%) r2=s_{x'╯į$环CYYwipq%99<5&
ӔNvl+ewKvkX,nW+ЅR͐w?
3d`3Y_hkbhݜgr89nr6WKkcCMWnՉ>V瞝k̬Q5ǟtۖ%y&u,c8A1TvHRhot[~WX%sB 1ێwǫ;首٣5	,-*pN2k{
.8Lt͉.'@v.8rr7'@ɽmc&q+FD4Fw*NKq>&x~VtS83}ſ\^5{=]FT6,2A._G5!B֬~,kL3yl	^9?߰ۭǊL0ImXʨ9>ךi"ʏLyVy2?y:) D\dK]2g%}%Wߑsv.</@l38/8<yiaok2剏ڂw,Rg2p;;F'Դ[k !yznݣhz}O<wLPށXzn&N)n/W$ij^f/d+#H;\n*994Z]4JcSx8
z 
|A
gdm%#16:w.ksy$1n10?]('Rsr;zMR{omAE#?!ffOScc7RM<ѼcW \wO&DRLҷ
yX#9>j rhnYE*#`2p6u!xYP⽝&FRBR=#3Goܠ6WRҼ(lبVڋ9,W0⼏Ys%ZWP,x9A~` ۀ@#nC̮_cϒ(qݕOHY^6S2Jh ~z©4{+X4aϕʭّ700~t/(o4/W~LI;w9k3 K[b.f&&0Fe9g;W~yFMǦo:w
٦V3NnG^6u j~Y?+ƨ|u E"^jME<w6!rѣ?WJ?R]
2K.Fm iGOrIoӏÏ0V'=O5Oڸ9Ӿ2YX4Ey_á`;;q]U틣A2DZ&
X#d<s_ZƛvU$9iHDl%XQ̃'8bI*9zSj6feǛy$A
'q5y?h:Rcs}=2HIXOvcrFGAZUB6=F/JH0G;CC2/7hfF*dpTrszbO/6AbfW';v،=!~03E3iZcnJ; d3 KZեǨ<^_?~~ϳot8-;(%$z^ j"itSQ̠m	
gN:f4!ƭfET"&~gFUVZ^zzn_͜8Eex5 KyuuM>^6=9ۓ?k
R[91 Sw'q}"/[5oxKye>R|DQ͏WiMo8"MJ$4J~T]3'I[xNK>KFy$$Rj;m5h!H@όXr20{py?^ _2Gf_2r!2ٲY E
уv]yI 
?Edi	Ӕ8?>2D.a~!>fH' iC]'*k)Mr,؆ ʺ)%érwh^ i~Ҟ0ᧈhF<am݉yA۽_u4&ZKJԫ|( m8</7],Z۽{oƯ4?jːGW.\qP m.$V߫˹T)caFz ዉռ%uK9}z_58Łqޮ| uFwt[YcҚIƘ̒3;{|Ѿ-h|H-mTYZZTȁ+z;J-P]$ZZ,EZ?v˸gz=#)g[fVkBKPT"RqZoT>,<]j xfg& p:®k> uu-8F\HGPG^;c}kGZ.o9]*HG	XW#giB scc>3 A^'rm;SOmrY

`;\x?H_ioDyn+Wܦק~FGk>Hc&ܜv9i8um`5gpw}K#m_X_«=MHI!;?
һ_.xov OMو⸛S="[j0CF?U+}OH?[7
O?z"d٠\$3  ] ojOI:c p8={x |~Դ/5+})Eԫ$Ҭk,	"ĿQoZw%{=""TȄ=uG'#$f}fI X
bg+
v^ \T-dlK{y!=*>j]smƭr?[!77
D(ڹύ~-4c.Xc&g& 2sО*[l__W63YY"9/M.IoD7?h(cML=N; ļ {⏈1U׵|7Kijܴbg$}3ǿ" zxN5+*`,dT(1~{U[S4o/a'̦K)ꍭ=x~ l؇M:גclY/y'=ȯ5y3/@~:LOuswouzB_r՜z| O4zUSj^(UcNU?ylX%"Rwl૾%X|гV">s,m"b0zW5|/y|Y*i[ #s׷C[jKF>LO^I"?~?y![.|$~) -kgSj^! kY	K=ΛҜ8+/_^cokXi1@v' rq鏈Z3_Q]i$ۆ'p33^HZ>cj9(؍CI8櫗f~5㏊+7o
x~kd r.CGy67W__/jZ6	f.d$9vN^3ְZa$\ n iׇ9leZv/b!fAQDԟi&XW\iԷUItDvY@]F%Opǣ?w;y3;`HFq0(}kյGռU}cFR&Z+:.wPnco_xzZmJC5\ya|j#	yb\q 
>xkEKm*`t .B#=o]Gyyt[7֢O%EP=H˶jogĻ=NM̚$v#e!C
$'IT|) 
VC7{kk

ARݚ:O¿D.|QbKM^$V#*9s qoj
ūnҵ>9#]DP~VGd^ }xIKK=
ORd婅Hؓ8QMOx!awj	/%vqP]d*Y$rl#=芌RVmu;Ҽ>sÞ4WoyOjm`IW[ E9¼"
Yjƥ߮^i{'nyVWi
Vo4楯/k[WeEu.1TI=F= |K/5.Lٛhf2s)^+33 6x;u4bVx$+t8gPA_: ^·K}6ymԳVnKu,	 Wxᵏ~h71Y1[qUrefuᎏKGXM>.Gvd;HggOZ~uޟ?ǈY:[ӴKgA!2LʫɒTP	]M*ӣk+tӧ
V.];WM
 	?%+VzI}UR=)g|E/Z,ϊnKkkA*D╊\Gxwᮋ]vK& P5G#Ha刱@<}ZI.RYQ.HҖM7# I0;SZٰM/mMO?]z3Sfn}H铃R7)߯z1ޕ 1I[_j>bӍ7zd@ t׎I᳻Hvm6}x&^+@VI_ƥTGĚ{j
ݼ&yI1jbh(1Er{W~"~ i5_b)<.kV7ZomghDgcː0Ik(E's:sV:j((((((((((((((((((((((((((((((((((((((((((((FK?Ok2JI7SAک_[zlB6mA^>aW?e3i:iW+?Y"H6)r3O5 j_30|OWԘGo<柦]o
;:Or%xkrdoOڏ oKs6k򥈂H8rkߞaygk;ݧ|;!_|Gc趗:)3^+,/Hqq$ר>"Y4|ant.l֝5ٹhB2ȗ2*f]J9G7Zޛui\
4vh%e?dA_-_oīPKƼFab9畦085
5 ho;oŖ\M--w6oFy"߂ߝzgmoᇋ4{{Boo0|y⼧xV:}rIqg	I!x){`v$
ޥH/sg{?_k͹&

GxN$\o+$WO!7N>_ZSOR'#X.//
(SY qe:¿2i:Mڋ\}#@ p|Q"z2~ :{iwC7Qq# ?.s^v+ɍ~rx#TMYFdF7)؎0{oڝ5HZ;r7}E;$rJVLuO~[>."#g\ }OS`mږz _0O1<1GZ6js>hZCjIm')3}G>#/߈c4Y]#^.F~P: gdW2Z׳_pWenq_GxX}\~ea5i#MUTY@`_.e8=<.xf:/??jg#?_{5w|P`S5x/i~ XT%d}ʬ@"~win!&W$1 X
i|7k
xwPK.8fSt~xrY_n_qn	8[;F/ŏ
51X O_kQifXH.e\v5ٿ:gz:UokXY"iRFx!$fPrr$KN~^u-
;]Rؼ;X.ww#Mz?<% uѧaƦ8(&g'm 2S6ax{-O v
XI "b'NSl-x*ѭ+YcpJl69	q^Y V4x^m>pm;>W|
 Ǎ&9tnap|-iVVZ(&x[_]kZOO0hZQ"o3k?
61CD.{	8y*68_Fk_[|=?ij\pOkΏ(Y
 #%W(˵N:q_߱duqk%&dk<rD(dqqQQ{ܼÝO> x66X+kVZ(RA?4ǭq~2ƍo>t[9>0xvcKئ򕢙\eX;
 l}\]x/<M}J3q-"Cݻy<C2"q f7oikboQ_]ūJFͅ`>a'^[*<\ v= lm>=i<˂͋21_
.5?(-J,Σh[y'hKg C3Sſ +o 4ͥj].Acx☈
q*9^cwp`QPk> "T:TھmCI[a0e+Kc'}-C}7 ?'U֙e̫|F9LMߖg|n}D<m^fit-mo<܎03Z?\W~ϟtIG2 ڍKR[C!;Wr@Si{-ok|\uK+}d03Mv	ds\)ˠS6NCxIme!MZOp5me:5<}*?m?R
rOZmKqq\$1)!*J(uuOC+>k$ ]`m9O8td&+plGYLm|9YOJ߲w Ȟ(.</,/Q(H+I#=9Ϯ%|IB״?C	.⸏x Xʀ@>?
x7(񥎵g{j2ioyE?ٰq*DՙV|W8
7Oc(*"1H]??[PƷOu-~f#s<w|`{5KGs+4?l
z~-oG.$DVVVZģMS:C\ZO"lڴZ@o 
~;~.| o8v)希c?)u+C<7&7>
̺NۇwZ#V{O <ssM4}yt8miRX޹<zפq/>x+חM.63L0_ >,9xS쮥>	upp}ߊli̐pV3x`y`NqAԒ?W>  z%ԾxCh[=B(# 1;Lvj k(anZN4[=ͲNHCDW9hnmir#Ғq==k f-Ic5׉([w	#^[+bgBVVng[S h^ }K}ۉ8 `-y^[]kL/Kё}_	Go/hmft[MRHef.~VJ縮I |c?~yu,/?=+꽟<y<iX OҽI-iAP12s~׃u(5wuY$E6LRFw.8ҿ` ~Zֱ2U]2 
+gA$ƛ4XIpōA[	?_3[	GNn>φ>2XԦBmJUO#jWWOw1h:*: |2>PsK%>=kAzN/,:?"8by^	v!?<ikwn<oi"z׹E.Uuw=Fگڴ]en$ͣrxJ봍z$͖R2=OcL~u_CմVݟ4c ={"e晽u ׮g}Q&g2
?>K// Z%r _/bTh&oJrY~]mc5h?4GDP8gbH> ȡy)/
Qot(GO@n
j͸]}~t5şkZK|4|n#[ZX-wŕCp
CtΆamKO[dHѦ n89Q^!>iC3B+3޺H[>'j2j	xs+g^nrˌ@+gS#O<k &]1H q'cs9&6}_tVC	bFҴjW&+V)BvK65-]4vZ4	,<#Iu.o?~,4#~,_Hn4& ?'ý
`ѵ٬,7~cc&I,Xq_Eƶc|-\~`y6WMj
jWlz?[º>қMK-pN9 Y㲯L^MO''0?&(#,fT
%8O,3ɌͫƷ  
pRrmg|Ew4ֱhk2U27C}+K\խX{YHDkd2<W#z<z?tzFn uoP0Apۂʁ{0<j ]I5k˗Ə^\C
*aad =k̼MSdQ{G'v:>!|%>uxwBhsq &(υ~˖_
Hd~RzzE_S9N6sLK325!YYr%^+[Dw:,ՖO6Z5BQ&/^h|cZi۪>3$~q<|bjf!ǒX|(L Nk(߯V>iH_KX3x?OӕEc s8T/6G%TNa^n]vs4}O)xފΧqtkZ95,%4
is&OQھ j+xDܸ] \}\_w^Id<s+hJ{gSBVk%?[ g_GǏ5<
0j [YKPns#:	y.,1^yW2 % \*KX2>k-u)?j94
4_;o62/Gm~2?q'A["h,VxMdX =.q]_R1"o=;JO
xJ V-W=2pM*ԟ^
z) ~mzZ|_Gg-mv? ?u@-VvA%#:<Rj ǫ"|Ws0
8^e2ݒy_0%q }Cְ5_n߭t,ϥ/KvwM(!#_3<z-6o2F9X\z{VyV2c 57	JyHtA+"[K6b>as[Xu~Y__EuhV]ѭe# :t[gXfZ0?Z Uj3/G2 Dɳ菜A~]<@<玥]߂o9ߥyG_گᯎ
]Cyuq!MoR@pqyƾfecEاN\=C2*ȯx.:O> _7cUܪsk޿fqѳLz^Q^!_>J&5  q: ǵ@͸ 
CfX䉡eEk18_~	hU] #EH7@Fp(,zsNSԿdk"\glv>y3Qǂn>sՏ2g5#[Xg&JkBv;ky=8r|?ouK6ռL%vE!v3ָڷ~/plX=x$	ý}:Qj>6nhCO#'~
u[ğ|3K"+C:ey]$e}^|j߄Gdo녊 `jT9c[jP77-h h_5isg|[rG1F%>a><~|3ëOj"ִO[?sG$I"e{˨CD "289x&z_۩<ĚU\Q0?s\o4x4x>˫j,>~Uo\mz?G
vgc<R_:hlN|>[a玕/: »;7 ھ1o&w4@9n5%Rof"}5(o"82kፆ|F4=fqq{fFh.wP8>o?b}u+G{XχR+mV|`zxO&Mއ弲=:JmX@o[&<?{f+إ>A\kz+.;fvm^[圽aW4kqS?<Gk%qq9#^~*m toCTkIG>*D׈/.V&1 -)& {?OG֋CdnvUO5 *9zZߚ|3"v~7CMkᕭ #;XiwS
3|=A#Ş"m[S(\)ZHT1ϸ>ǈ g3w~Aoo5vw~̲\9:W~ʺEKOm7P1݅a*/T}WgПj?	|	- +rQ.=/M66-f$^׍>'j?|xgZeѳCH!dVBnoυ_yMHώBTע|^#'/
yFmMփ5iϕ39V|_|WⴆcMei~\\̍qjaK]\Liq!zOGOE|mh:\[vIʓa3< f
Ks=Jj>%
|]W# 	gx~_-Ƒoi#EFc<㨧v[:Ƈo.xvxz\Ms$amۙ vY>{>WukK=
!d|| 't~12H.pX])EzO"GlTmP{]<qʣRiKѼ0[['c/+^0H-ǥy߇߲גC;׀s	qỖ cq$t|+5<XY}Nc͐\+g^@ eX|+=[H\Ke_G"Os-aJ[k28Ȭ-ʥ7-/υQA|=cY&Mb-4T o};ǿmͽyKQH+;@X z^o_/|=GGNRn]iwy;`|ȁ G=(<[OjM#S^[K=6
=#t; `sֲ^f_~^#VMڅφ.l%u5@?_Ýg^d4}CK$Bc^8TV|@3XӛRhNSqݼYo+8lnw@=/;xPЗ[SHX*$0`AH=@'mAxWH yjO5?hw˧ Z}o;`GxF+'^]x>'|15;_.դՍm{28<Ȭ[GOj\IH8ugly&mM deakkH1]RzcL4~B0p h~=+K9-EpZ 
0 <y+_gᾃg{m⫶Ik9Ysu$c
:Qk;{P
Iu1EU?(}<?~
%PǦgȱG/ӁS%/x-%yl.>#Vֽt%P$m!ܜ$~>:Ծ Y~~wb^ PYp Ym607`WI3|-Ԯ!նX㽄2T{r1\ {C,mdv<l?Py!b}ݻ;i1r+|#GxJ>&|?ޡg,l)XGċ'o8O;_-tubgIp\0HʪT6&O>n{'TjZS-}P>\|8i?oC:U|d
r1TMnO:%7/<Q޳+-mR
pjoС> ͟?hk
ZUԤ{M'XK#X,'qO|M>Ӣ+( kDyU?QNp1E QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE WH[, 
uB"?i#f?oZ?<7pb=Q> _|+sĞ5<AkkgoQOn(˴Rt_t ] uzi:  Zwo$GMA#=}fG?Ct_뿵#|=[kQx7Z^^Cc4lk2*/@3Xc⟈3xo^:ŮYmOx;&*20T+ n>Zn<\]e
5zWyoil[;siI,w!zQm#E&\qdje<U&{|S1煔P<i]]կ5M{ǚmuzi:N%VO$<!aLds[/{RecIŴA`(aƽW
{$Vz=  6h.p -ʎy㇧mN?PO	xQk>,Ҕpuv8P'<9iPy0IYa|Gv#לyiO;MӭmSѥb(ΚYb3? l<Adkڣ\l`RHby$.9@PV\pϙz[ ֿd/]kIP$f̊XW?
='ÚR;f-!{K{|nV2yB; V(l&&+% /<-ʹqMO#ں)]Բ9%kSￌ>|;'+S$Au>i[v+YYO uSM|D#[߆Wut?蘬o+>v?`+Ↄn˳9~8'+oh!{<:U6-#5Y6GTVW54  z; ?
YĞ[I7
k4y7lJE 3
Ϸ8^܌ Oj7)jPƶk]܀VN.\*^9mo;
ͦizb8+bV$t8 ]xa=sD.B t^ŚljcL?ֶ5Ս j ҹ qV<)v6x>INx젉ƨ&p	<:|\jx;=B]@ #*d
sc޲oFOXv,K$I$^=-\ִ$8f{]Cÿ&U<IïA[5*:¸i38J.~|QQ Əڦ)$̪37`c<J;:kz=[]_Jy
u`<S3cSG g^7bmC<BA +c:gfxc:=hfȕ?F;f,136ȺzUfC$wp_OZӦo
17׷VPk1]ZIu
42Np9ymWuNV> Y6-l&e#!i+0FI]y{.IŲBdw+Rߕyᾥ_
kT:EWR hFjnRw1z?~Zn]z{%ͨmoh`r6yXWRSi{NߗBߺOJVfh$`sWH?[:l_wlCM[5 ,.DrB #A9~ʹ~_sZ{iHu]eSE#+\dT14N8n }3_S]4Y[;gV#?{Jԉ Ѝax_a8o{\Oy;);> x#ÿ$OKMS\MjRdra^w 
CH\zWys~YviBA9t{4dJRh
SFmBOORu&d "=:61?1~O۪KwͥO'USOmr<^?|9/j j[a}FV.iNzbsMxƗ7Zȱ׼J58.;l#dSbTG!O*I;6*V+{?^]]hvvYh:ΓlevY|iBk  
9 />x^Ji095Kk+ZY	 v@p7>X. q[C>7汚LQH=#8]_ّtx^^wi
73u?CoN|~0>x/:&7o-A"]f+_B:C:->zRCˋ]ߌeᷞ)^4o*3A#f
K&6]Fb>HG]Gquܬ~:+*4KⱌgҶ$Kik*h
Ubs3m}㮍x{}"9(Xa/瞝/׏ڃG5DG[VͷX
 c$| |xպQE<J?`V|vzio#)	 %:n9M#}fȍ|BX`?+_[4n-6"!v
T	7`n*s 8Kqs=ɿK[ sϵoh\hwGm5K ;n<ԏ>S*IbTTgMp_f.}.;bZ6/;8e*#^+{<K[l^)c,H wR0
~xGu/-Ԟu Mg|UKڲ&O&y\ư$SIξjpYn` ИN+iDlh~{ Z/#  g'kO~!ڭō $|L6־ i<d"|B\x{Yoa!»!8'kpwK<|Tj>?k|.m~E{-Iu"-bE $/sN;q?%^]SvWt6hoqē6 ~ſV7C
v`2kdܕf
]m7R]o,eZ ܓ+8<Wu#.TzQj ~߳wy |qi~.^}U71ۖ d~_ShǋmOC_zƥiٓGh3r\0ڢݸ h-o)!dmN$Dvɯ[~ lc8HViҕ6QgI<Isw_xAAw-5[*IVZgð>"o4,Eo$;i:)_A f Akd_H4 Kϧ4j< =:wq=6쑷
EKj֬|s[/qNb+2@pB7#qO3[񭲛?
V> W?]Zk%o],p_H^_'Mᯌ:
{U$U[#eXo0HvF,e*I˖'h?"V)V_Agc;~í[LMW?`wZ9~m?7y{_.etݬl,{7>>i=ցyZB=֊lQ*69̀2I&B,Vv w+ɷ[YFejG\ּ\|?~k^!A?Rji_-KGY[{sx-f6U!A5O5[me]EHWft Ļ Y%K2]V(!@Ѱ#17?Q <Mq+O9	 a +j«4h` g|p@#ӱ޾O<5I neK+:nXZeP UMl1=.un81<ܞ>>~ǦrYfVuP_Ĝzk]	?xmuoky϶ZGk3ZXeF *++*	^3U~䒏/֋Ii ~,bk՞xx/G8o(y 	3GqJ<ރ.GDnmR+N8'q?	67|Em\{xbVp6w :א_H^4O<.ȇyu?6I<+lSK*eSk~!F[_BN2ȿAw6n60/ o=JPy1;0DہN'5
IjЦ]D7HPN2z׵Nbci5jcObla AZkoC2\xr<G=k :^2a+d|oG#yj_ xo/ava9cө}.A+Tggn:7K}g_ܟBwWVyEo?}dkiq?6&c,z=ӟukesVGʬ=N  hjh-`m8~A'4Sƾ.IMR#-2X6۹H=};o	@1 kh5w	»&ާ|3jRaIaG<>Z4{*sVf/	5ڧ#^NـT N㌑|I`𞛫Xڴ]
̻MxR Vj6>
I%ouٗ
g#=@\84<+Bez2FW X\x|
Hs?~!;Z%*FxV3:Wџ bbmn-JèXF7mZ_] 	;~.VY|K vwo4,Vjw/ʁ:sOZ(S<:GٞY-+L۩Md"A{[Q|<lgoE~pNjztW
iN#xtr1/YY$lyW_-OTվ/kZdVu$K%xW=U9-8O5ֱ4lV~$PQh?ֹ_!׼a7oU$CWo7NR
ğ|OIp渽4: ]Wג=_TY9b"	玔b ܏] #|
#$> 
O 9/"ƚ"S ?>|'qmky2340yJq_\;v|NM˂ej7䀪*e$i
4z/[ .p-|-w:άouq;bW _?hXEqៅ~/|\(\moq^Şh3xz.d0)fNSYGzVg	ӻ{YOz['fӢi-ċx|Eg֎IaeZYo8#,0gNo_:x>ҼQW)
S͟-dTc?YgfWTc?zŋvۻʽVwlcap?jd=[d|[	}[W.XNL K muۚhB=;hn&m൵ q}`{׻~Wjzܭ{7J?Iou>Y>DtoXG0jVnOѦx|?4mm[3,ƃּ潃ᧈѶ}
yO
NC[9q5|!20F]s>xkJ
Ǧko [WW$[,n0ɟ>0񗇾(xM|[ZY+9\g\ӿlZ_ jIwr0Xo)L
*x))s\27xj6j Lb.T^@=&'xúW:ƍ=1\`	o~:k/DQenЁ ~ʊi(ψ<En?9Ԯ.rnkxȷttJֿ>
.'
`M~՝Kd~}+xò[z +kI)C 8Q_'M_cj]3@<6C,]Goh|7^qk
o䋙@Aoߚg'ds*g۟Oռ;gXx Ync)$<3y#Rr㶋zL:e4KX$@{
mK} $ug%і`2y<Vww_SKuK{H gwE+PHzƵ8)?Sߵ/톗dofebQp0ރҼ
*\qYMxI%EMZpdG_=}/Yh4,m|#$#Lا,Ai]O
x>ݷ/8L{VSRC)^CQ4x~K{k.ۙUCyġ#(q?мQ_ܩ@dɅ)ryJ??6#	/IY9}{Hm
"ޛP}Ԟ: ~Ӊjq?
Ϥ̐\F3H(L@ #i$gJMC+z
7e`l{$b	SA9_#|Wmm3M}qm %n1q_.<Yqo|_w^zlj. Yp*a᷎<McӮx 5.T
ЍhSnX<՟JNȮOul}qO_
ofTk醭[
=Dl&V>?x><i|f-;{D MRÁm	3^'M31Z]t<Ms>C{qtPˠ&<wc=G4欑ms ՗mOKyಘEe{\"vr+ft3F־G{]A-HDU	'sPIЌuϒgV5AgMmƱ[3,$:-3@AmqkkQմ 	"j[V}xTn_nLǚtShN>LI= MaֺkԱzz js
*1t_
ީ]iQ\SIkmH	E*P0  /S]ʠgpڿ<I'!|*\wB5Z'l+t`y;{]y b].|D+x0]u HVEko@$	h?ay?3yWnc~"]vS&
ĖREiܹ#[K\i0mb;6I&2|dޕjǹ9;{m,#mHw
B2y8|'TM}%퓃nlWckz|,:im>^5-o<3;*H{;T@3My|E$6quLYK\G4g
+j/ᖷt1&0Eq3ILck ] Ei6ip~Y!QǶ|VҤY $^+dO5-as{OzTƅ<!.=w7ziDf1!!񮃨iZ]i~V-RVbe#pۜq\Αxx2>#Jɧ%߉e{uo+,E	
F@;w6 ֹ_P?>	`|3kti^k<,DFRN^˖H[|V]7C6ص}ܛ!øјXte|eŚ-"RmJk}>;M)uH2xc{ztO_Uii[۪
kv=KtiIjURia|E9<i}徣mmi֒&ԁ,s=+/Q?g8B'{k
%v5Ps|~̺
wo4!{ }p+ZKAXF+ΔgAd={¿um4)\mc:eeYXpJGIx&o+P׭$ib[ۆ9!ֹI5a{L~&0 w=+ZuVKce|uU8\MX~v- 7.%Y\l kH\fG[F>F}<3kqE
sq82ӯ.'RV	W,;i;{;uԘ4īvUZ:Jm'&JqF#YTPxké1W JxRߵGy|"E@-A̌f  _ėBQ\EPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEP^_W-ǿ^^q|8+2c\Z7+G
IrqK_xsQv 2'u.`/E0ܹi`l)1  &E75?7?
^k$񡹵14^
(8]屒nt:utPڧ7uu𷊡mƹ?07m
Ht 	h}_P|;.ig2i$w%U  ?l|#_b70R3ν75-uߏ
k{m4;V)dBzVQ]5'4n/7:
]m5|%98Ĥa+>!
>0|u^|YwV<*o|i.ҘR߆ qg|6u_bx=wcq3К
3a:nrOS
ɻlѥJ\+nh'#,n<?gkw1\jE+on *<C{7>Z?φ>*F+kpy"q}S#s7lu~麅sgݖM'*c#iҼ#wW4*|^H9%T){H]]k}	tk\w6zw Z?`N+ wɥ=v4^qYq_E<Tx~$̆
D
˦>$U}Zb3sƇk]N>6zSN?|W&cH -^vCwQt.iNyԫ(rF:[r 2$:2EFE!8y 30Ot41+'łI8Џ(w^k>gx$GGV(WhU5?uα~}2\ .6Hg_1CzWNg^SՇcQ?[44k3ڵ,z-@Kc'Y6y
#HJU$g?Qt~tkjw6%ڕ<q,s?
le{cx#CVf{{ vcEFݜ)2h?At淑&ܭƵƙ>xZ jZz^'5IQ@gV'8k3Ea񗊗E}(>}l.H
3Co#i7q_PV#t |_־9lcz
.? uovD]Tz}˿U-ב~͞ mukdEGYMצ87oGMNXX_ȇ=ɻv8IF_+|J+U|#ۺ\[#d1(k' oy#ZٍƔ`	c _%h_"xvng(>\|[*~^_B?["?|9v3EOv"3Y`px8 ya
z﷚=St9  hv}c땊B=kǼc8UyUH\ܨ 
g8f_tKW[E|_61=i)@FcPO|MW/{]A{%#GuǙ
\+
/=RKG xROhn%mCh	F⯎kzl# 7u(8M-]=Bo4۞ /"^h>#73xtxF#IQͅ;&Lׂ>+|֟I]>q,f6Fv{W^Wՠ[p*S&.O	h\iv7w6#{M<c>|2~cu5a-J+qOlj|*~(ԣi&{[8E-r,pK\IP-xG-cMZzԔٽ:K,R\u;g{tiQV#hɥuO!o~.Ə}w0^G-Ř$B0įg;Er Ecqh:miwcknO#*ʬFHc5
L5)fxLP%ޫ.N	  
Y8Ve-BNbT"^Q*#KiZc&+=0Z/uˆi5=N9UdYX .޵7=?<ysChRi~͐GvK
F\8^;[kW,7v)>Sx{te$oۄ䜕k5bL'||ID)4l 'Iˮk6Zu걥Ũ4!e\'J>:7xoOo	zZn<eߴ!Yc刾@^r@q_0~  >)Nth~]#IyvdH$f!9_N|Z5 IX`kxֵ%Y6Ot nDEƤ?r~YIW&D뜐GLgiq"I"wo\
h>$<YMzXHK0t+6a ga~vxRYvsHT##1'sQ9z~G
JnqIZ/^j,VoF\2Dvav9 )|K~&#~y)+<Y/w&nM^.t萭& Lc@9ylڏki7ggܶE*i.[|V.ye OٓJ͠o^5].2X>둂++	l~#Ivi⫩lG@%۰#/ {Կ. dx=H)m]rLQ t\?t4:T-g0l<y gtzXƴ{|G%|C f 4{_7S վ>khįџ*q՞&#-1@gox
^LdNVmWh`	`jER߫/Fr G:>m}+>$jz߅|Eu$'ӰLkA~̟N/xtbMslGu_,8CrO"qy
W#hW{8pK~Tu\vzb%o)$ Im-h7zouӭEuMܹ?\:x_=2 H%Is*M5ȉDe|mFRu K mtU.ٛrGn ^
+|'U˪:~|q Zw\ogE ~ڧ^WW-dw#
)XW.I'@y}OzG 
umJ-:[K;`H˂̓~q1~~0ZF.O˃ ӒF8	 c|gmK~
I-l4W<.v
FKG!=H^ryU:zY} .~%~W灬4=bVmf(+ U26~l\|Rt>?5femuxX.%BEHs Gρ<ռ:Ƌwb,t?]وiJ"H.I$]^4?U/ghmiok- SdQ#RRVLpT^]G:Ɠiý
rÔ:}ܿ2+Qң'N%8M$簯+ #h W2.eqsrghL*mR6#v:Z_Ϸ^r Kn,|H-ɼӎ+Kl 9p`#4in*V?7o[1o/N[8-Ҿ16i'h/^( ~nm;knvBgkm9rH9[t,fk֥e|o?zI|dfq^	}zcnK]/r ϗO,J~botZfSXտmy4Bk;r߻'&Eg{̓H;W[$OHڣ:R5Jt5hY+B__kiVڍڄ:M%ZH#q
 #i2$զ6<+o"孀gX$Я<׼ (>2y,:>Կ?J"5OGvwEH>uψ8ZݎTa;tgQknIA[}F}BHH0@>a~*ŭn׿f+Xe|^D+ofגM lT3t
_?ڥ~T%5xcW&lq | "*oRrG~ x~|Ttb/ |pu  =jxO ~ZJ(P'Xmxvx.q2ۿ: g]nk
xzLUԤ#;sTuH(Kc/v|}^In"$FWBH$rE|{ksO׈َ3f }oҾ>x_m6<OH*E%@@ヒ85IE|Xvm,-;%97ht|v:rk:'ucdϚ)!R}N?p4z?Ûk}6sr  O,~æj^߃tȶjOvRFڬ]r=
zw~C?wڬN颋R
WhVWC&2[ǽᵛ_zUKK˭<] $uĚ|nYHn+6F~:XéXD״ıjFC
g_Y|ea%Ȳn_4ecŤ%q$ӫ{7&Y].mJK+bVX"?.i')Ԕ951?-Y 2KcPA-F!x;.IcV~|3uOqyktʮàڇ} 5K_:ci~	KYԍ {xV'!]-# sॺG[Ó J)уR\>iN_kck<5@73,wOSs\~ᯅ&zkk?:r	i۱d^:M<U/émSO!icT
Nܞ>}+qm?HK,X-]Df fA*yƼs"G{c}"ELֲ29,-wĺtoHdfSB7]OAEhvS_h3nZ@/vpB ֯/5|?\wVA'$~'>Rn@R&2W:l0~3ygN^{~=}OZi>(x9mtquMzW#~Y뚶⯏&;/4+OxdfQ
Dl[G<sO۷φ~2xxF^׉<phLc YFEJ2i$K=JÞ}:o$kWڅ%HNC[8| 
k>υn&k"O9#@r u#'^m/I~Pl"ӂ$oە=SڰV6Nm٫|zռj<ok]jrO }[9m=Ӽ%z'	ؿ|SOmۧXt 5˪ߐOzŞ%ek:g~0xJRᮡRZDnP	'y?G×V7-'<Uw@_q qaU{}Yu<_X|I/oծ&4wR؄)lslĎ#5W_;źVu:XCh|9q0^	"}D39q3;oukVL7x[ˆZTBqTrOo߉
hq.^#\$Brڼt8'4<d-.k}VE
r\]}mc>`IXws=IhIkG^jonڭm@ZI{y)ԏ&y9XM/.mL#]= 漷Ԗ]WbZKf>[-~A5KRN;#uo!S-/i
)`$_@|c_::wqt$bb%1.ml.9eg."[Eoƛ K/ue!K? & vG/{X|f^N?ξm</R>6aڅ)1ɏzfKff{:3Y 8Mz?[YcFr?xM]ZFuvߵ|[Լ3_i:M^EƩtŢr}c#tvV
WŶ}蒈vDWh$~׸ЎFeU
? NI+پO:^GfCw:fWiLkgibcī8G:*ĩkԍsH?1Jya@2
rOKz ){]jͧo= Xg`vv .5axͦX-hw	jDJyqς<1_^x?-f oxMO%\0XW	8%ՓMISg T4hZ<l̰@B'XOdU7r{u^;TjRφu$sq8$n2t ׁAx,^v>1o6z\mdXbdvD"\	'ݟnE(Цq,.Rx8G!2MG6&XI gwA ߈Z>!ē_h-BI^]Q0q}+5r\&~H*-<(Uo R4/k^ZSu
?-l|úaT ,Pp?=( O3#.,	szğO⹳_뉡6,:2$MF|ْ(5㏉tۭIɭ%k
9`Zp]"L y猥$diNNax6Pk`.w(CsYUyֹh%6+KZ&O0[J]w
|_x^-D:5%q4dxc2:cz `Ngfڧ/J>ǦɆ ;ϩ4:*S՝ׄhۿ-,I-]%-aH!wFG99- ,mGֵ_[C)agxIR  	=x- -;l<=cΟ88> W|
w6}N 5K;]tP7e5p-+u
ʿor
0< <O*|B5߈^6G
kI+Z'¿jzi~.KgẀf
T:r(*xo{ٵ/4uMÎ?e#ʟe8Ԛ_4:a}icj9ǟ>3'חPSDH0.\O?j&}g|DjJ4[䁻
7ǝm+_-
u;YǛ||SeZT?@č)'Lsnzs^ڪMLӿgaHlU2%rHpsk>
VܞusxO)NF)\g*T
Qz|`e 3*PM嫃wҽ{.ǁQ@=RHXu8{e⫿x+lن}l噲"EΪGL%!k
&Ծ"BV
Ҍ w?U*nS!>6G2Mk>/~մ$luRb+)9\}-S^$<M"-ze2kwR|̝3 /c$O,!n
<<K_9g{J2>A<Um'?#5;g>Xn`h+y.5ˍnlc3s]GJ;QnMedds<Y߁~'xwO:ş-yU%ѾKeI<毖OV;|=5}ugn&ַ}e&m$QfDhbzj iHƛ|BsٍqxibyyرW c8?J*^ïjڕơjCE?JnFrd,{g9T~)+'Ngkx xD҉]4J-^}'n\]JO dNg9+QBxo]/
 PwZlrFBvMrp+s᭜-,M"Y ;r=g~ȾᾏMǏV9 kҧLw9]B|7=ֵ:ڥ֣ȳ2$sn+{xĺ-sqjc[hAX\#^9'>=k+wk;8|y.<Yq]dbvIWU[x)Io.^l98#ZS|XKKkׇo Ԭ۸tR1pSikwWDW-}Z6t 6DFi(Dp{+]C3Ж\$`ʞJin=	IuDU"'T""6sێk?OG77zMq\xwZhyo T
^mO6'6tE(4
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
_leϧE[)V*1ZTPтv#o
~
k6鶺MYːZ''_:'BEt[aWn܂?P+KŞžn o{y8R5g;"/P.a"pK1*qc=0JjTUs*p(Uݟ*I"|C1xZX+Oi
>ߵȶ+g|& <y_z[Z&ok2YdFHȱ.pF
[	~~ס
F2Ml%m*&~o~5_kSVwifZ;BǈbbzΊ83ȥYVWZ,/?6];:"ʧvL˒QI rsGĝ7F<2/[يXeUX#Wʾ'fRhSEV܎$`O8*;?XG1VlqB5mԕ5Z  g TjɬxFdy@SAAc~?~ⶃx[⏄uqn͕Ε;lkb+sS?P5j}=Fg$\\8BW-n S?׃9uV۩M/Qܫ'1 u}$z\|Ui
j7P2v2?Ja:ȮKᖴln/}$F>$]!NH:Z⟏<3O׼?,Mgj׍i#vfPS:{ p>{Id[a4
&eba֮P+2ٮ Iھ
;V{E	noμce-`]OB߇4ao%O{ į/6ŗ,-S[X5qc	˖&
0'w <%>h~w&m`CA5ޱU }qoMBuޚɸPXa|3i|O/lդUh*63P@O2&U?1U	 >_wR׼9sq`WNtTYNa's_ Ck^?5#K3G.5B	F:0,i'&o =+ 8%P/s(_{j+?JO-M:i#;
pk fb}#?.--M#hZ31k~%ۭij,_`0$fHב;TdM%;7} $m:|Vog?ि?h}ĿMu=9C%gOZƿcj~y}#1DYY+ ?gN+߂񷎭k?j!Y$0IUu!
O~`ʎtTھxWӯ,б͚D0]çj4?(
[Z]!&Ici3U`H$Tc?>8ҭu{ey/c̸h	c#iy=k[RC _dz}ЖI4魓 T3Bu6穔Ӕ)8nsૺm牿e-/Ji>( uԁsX𧏭	 IHTpV 95~ۿſ  x^*Wm!om&)yU.U^B G-dO)\y"i-YB.5}=Wi-&05ROS?Xé_gYM6򎇌>y?i :}o\%H% o?Zߵ1|@ _Jŗ8.bLGt"_w;B:u7m|Lj]qs=#Sԣ9܋_ȌѾ9`gSe8w#57-'݇ a@_ x[Ti^h>PY<FU_25ASy<c"x]C;74yEyf%T9ocfvlsڻπ?SO:_/nO60k3ʃR	k9_|פӷG`K	6uhuTNǒNW|M][E𔶶,|GDykg#h$ B mO,u+FJSo4dbg2EpN~8I+ֺ>|d~;03U
@-뚇mCcŚ;zb Մ/CCV4UZ9\aZV rK-kĚ:a[	m{1m%؈/g&x?}ZO<ibuOW,#*$C2rljoG4=Y|?xs$Z~$=꿴ƏEgg "L 1H[^ 
q
VNs:Wvc<-	c,|m MdޟAu8ݔۓ1?g^:ԤKH+"[׷
Sާ$c"iO|]Ηkssi<ɾjL<{1: |+_
>0V 5\%rB$#۰aT (,Umo<S冯ch^ |xoH,/tJWI d2LSeH#k GjQ)'g|lsG9#q>'~?x֟apF:Ɖni6G*ǐY<(߃SovjW_3hS2I(RDXsȭ%J3mM?#(T}il&pk g-_ǁnZ }Bg`[x5nUN Tv,)*LLs_x<ymx3YA4:sh+m tcZDkvTs&OKHݬ.0 "+_Ix"x>qBNzW-!մ٢?Cͪ6t4II*d3`NH
ѼUᛋghu$bX)H8ܭe(G OM/#Cs.F5[Lw Kv7 xq>C+[қI?Z ǧ<_ԣl,ٞ{WLҿo|(X_wjncGU␖0, 3oY~?xvk}Ej/#cewҴ&YZI._x?#|n?ɴLf{{W(m3~,kw꺥.[9iDptpP6Jc8%wx-k)&o.[xΕ4;%dGuFl@ÿ^oy {V -\c%BϾ&v99m̷Qp$_(cwJ^ͻjgJJGߋ~^75(lծ;y?cYJlac޼ z Rj.MRkgS!M^W;cxٱ:	 Ii |C⯱|J>Ԭݰ	*|_~ S⥷xZ[\[j\lO\2;cp#rJ4ZW5^:   ϛK`oMX|i}Cq_Pa{OvxJͮx(E2@.-83Z_Ş,:t?H/5]ZMn>Φ	KG,SSbJ'k;z}yŮo
f|srC=M`~:P.y'_OI<yO_'sO
\M_X:iMvz2`F oاYη?d,u]NzL^^ڽ%I8UU/دF1_#>ov4~-IMK:{߇6<{%}GIX,KFn	nAW "Vuu)9#/o ~;-X|W ڷ3-0$2p Fl||+.ő8,sQ
zR\ݏ"Eeos>8 /ď}x:}49nl?9fe8H<WǷ[­
?
+_^Io\ZM߇$Үm i^$Yh	ɮyINelo%/xC|+i&b}0`	r>zJGktLaDC~%ngqd󏅟^#R7Ki
Hg+noE3/ꏍ TO~! O;xKR(##"4O
1D	
0s5zJRPnڍfmV4T{JeD
H8<oI#.xsW\g83x<M⷇]>[M;P$Io1"mT$+`Q
1:6ZK7XޥYgx222!5puFZ2r6Dd]}B1N~;].W+fwrHF5G#eu?>Ft~Kx9[9A$a!L.MzxĖ:wK?Zj6sCt,tgiciTo<U+;GQ̺\dϦ~qVOhq8vS_g|Ze.s/'G~ăygUٜP2s	? ?V4/<Iᾒ<~%`"ܹ?.@y_gpM*Fx8kfveO,-6+.[v5tP[	i1,Y S (O^ լs5Y&33d޹A⹟F&Ng<CEi9OdW7/Xe@)ԎV<iO[UZCc_j^^E-7PqA%a3&ldi,- G7GXz .5McEsx^(Ѹ՚8w3vd>5]gǾ^% [dG??\cx|ҝHF7)S潏|`|rm~U֤wRK4$+ \cs/9+<= oܯW tcG*`t}9+"xS%⇉@m^8YY* &ǔVލ oEu}yjZء靤Yg8`109Yu!J~#xnƟǍs[;Ya\3d$An9;^>Id&wV^ZiO.P<7>pKAϭAN| &l!|iZXPYl'zkom!#:+y!QXM>*>-?J'<#/.Tȶ[B1M.Rx LojԮ-rK;kˉfwd{t^ "qIj*`y$ď`־LOj%V3WGmM.{fE'lLg|2G4Oedw6IO:qycRG?tέ+*
&
=tx:+uI$t%刪)9XvtB' ݇Ox E+xGE5 z5W+HJ1K ]/g//Hu|/Ick*,ȹ|sֵ>/=~ Mjz|/u MkV̞mמ2	yU^J#Dw;Aſ쫍b |?sk֖^[Bݦ318X?jO&5kχ/y"YD!&#qx
5᷆ckgGMi۰HY U=It6BfaIWm֡ +躆kо95kj?}5֩st?Q כx#_~GE%{?Fr$͸^iIkixzIlb5č88+HԺxtQ 7w|A~ךS&kkwkH`k]BaH<ǿٷ^?:-34q$J$;`Cۖ %<AY]Zd(?5K_9i\9'95mhmhq<f7XcOttcZxDӂ?7	ccM/T^@8$9*Wz ?bh-_XKb(tǳI$GV_FA^q_wRl>
m.ʦrAk<9  OizkGG+kZ|,Q |0  zsXл5f1I=QPQB)|g%v2x&O3Zf&a$Chv$ UQpOƗ7OkW|tVm^@{M|[}7]aGcppL1%)U&$ s^si7uo#^Ɇ^3;t\dqi?B+о	2%@Xdedc )aΰ|5&MрVXUsaTk|~h2hn^ԒHN	{eN<M	Ց_i_ğZWI
O-jkX4r\yEʃjŴpz#qޫEsiM$ZgnEx ߒTwƺ
@ђ܇֜-ѵ	X^arXvkI^ɗwH^o?)|I> svy#[I,HBFyc[ LG;uw7*C>oDquUKWuDi"\뷲GHF7.sJΔeR>͹>Udyέ8x_H~gi,
a`RUV`XXI'6ӥBw%~֬{mdcl2e|' > C\ͧ2{74gI|G8	)|a⯆>=o 0[$Qg5Q]ͩ|ֹ=b<>Y]8k'>^7mt
CI4k1y_doń_a_R_^O^(/<<l?*Eut^y uc J-_PfS+ddǏ5hIe_5RA$Ƹ|bLqMY5tgOL?`}b{{gϴkIʡ4eG"8s]Wo>:/xg4E[;=AyjɆA <$1<Q i>ִ<?y
Ccl<WA Sji6~/|LH%mޥ<p`#H#<;fԩ%u5-ec?
][4^T0בOdjX$~&j1+]B]+N	h.#I
pWh߰<3IzJMk<xV]X*xE'0m[GҚ4fV_Dfb1O1<'&b.sֿ߅tC]s:cwmwovl4_:A1؉;'YsQ\v#?3!a[obkvHcu,1oWgaAǯx'ΛqXGSVjV{i!Q\t^x>OBs,uxٙT~_T{imusmK fx| /鶺YS7qf-	~r{_xYխaxKkygԵk,*8W8'ǅ~ooy<+[FI$
ҹoxhkj]6ͧ*`C8Zєdʴa>u_ZX+_E;?40 $OֺKAV׍-u+k4C{# Wa[WW?Fֵ.dJlm\	ymq<+6> ݢ]kc~j RQ ֔uEFѱQI4;Q 3."cU q^=j#S7o2u6w
tv$g|%i.?TԢt
9g
cyV(p_
?:?DŬw]y*
BpvJLmOV~R|=(o\}إ_־o|"qol+T-j +
x[77#BxMyU2xU^AI$j4(kA[ߊʯmT=aE՗N@,fu {3LWC`7(
wk*5`<W~Ӿ4Լ3;m7uI,KoMJWfYs203X[Vhv=KMkm}qVv#s 
|OOg5ًȵZL_gA<r*G|QǧX
g%ӿ;oU\$!dxkw6O~5WDRL5Vi-|hgFR*1t~~_
5m|Y_lUnm|AZIYP[{g8$g&KT[=ԊT \#A	k[+CZ^^R"=ӗ>T'd62ÿi2HQV	 մR1գ;Ŷ͟|-oڛ-浽
pKLhZ')ZOu۹	#mΠ.+wsk}FCz[In.[ɜ3 Ǹ%kEV,Zi $&dG"I[s^(7~43K|vvpл-T@s5摦|5[?W~FE<=&K:f{GӮ
i*]i7'#v}vaGg[7Ķ=A!E%>H91ҽA_
DcCn=cStSa^IY(=?@cEAEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPEPE:|-$$H$8ce5enE|[j-m׃[HnLk䑌[7:0xW$$r1ϥk4-HknQSȧI+27-&]6]F.6TU#9+N1\8֪ДiKczu*ş7 eo#nWkYs~/W|#O>RuaڐY60i	H綧g~ mt Ucѯ$=hHd/zW5ৎ5XjZ]wzp7ެqnF>`Hܼ~\\/)xYJu·WN'izݎ&-E-Η=7Ev%LdW:%+Ʊ4_CZXg^W++dsqּ4oP[;6y͟]wa&]6|My=5>4k[4-q;֪ThՎj{Vj
u;ޛuavֶHʿA[7T H|E2ٮ֯ ke++gZs/ ?~$xٚjddw,%|eVwZկ\G-߄`EVydh' ʝ,<S3
9>3$?gqo!%[|/'+?xT\?N[($IDR+}kOŏ%dky-n,/ram(+gar?-OIӼ]HS|HQ|<ӌ	&EJxwj:k~(׃T6p\X#I,  vD.n"GHZD#}.+B!Ϸ%s^cB~,|5p:GptyaA/"݀8$kxS|<Y۶F;1Y*@nn#u k<U*mF(ΌeK?>-.m?vq#_]B0R`~:`ﵧ/_Xvrjq#YרXۥtdr0w3IϘL9$g qQO1fU{	s놶eVQ~~NlmGďX2^EXƏ9m69@LO<f2㆑5sU
O_¾y:!E2ck9mv[)sJI%HI;׹Ǻr1Qj1g&G3&OIFG!oJ-w
FMCOY *[kw`$Wğ7ً㾃x⮹x*P};Y8B$EmbA}c7_[A x'>oDV(hIڪ2GO炝7k8/$j-
~H|?mzvW
5)pdeTq3_ox[ R]Annr2,!$OQ]o |AA|֋u({gh(BĽȿ}zGv? k JTu'~B-nH% ,+"\"$YR>XMO@>hķ7VpFc뼾Oz ?h6
R96iŐCbgٝ_H|i|1gO4ߴmuGm3ĝW 9	y~Ӵ{}~R[;;{B̲ko2 BRO9NQpyg ,Ou[()#7;7n`,z'ׄ|1j/>Ǫ|3,u+/a4pFѓU9_ fH
Zh4N8#\A)ryAצjTmO
^snNdhrȪɹF3 s\yuF}C4 ?ں+C~Yj˲5U_.ԶI8⦻4xw#C?4\W
ĩ'L9_ZgiQv	%0ǉ]<)BAeiP`|T>.ռW].֍m^$
 $c%4 h_K;c_fFK+m:$ Ko#Vʣz/Shs~.
#MncsB]%r(I1潇	Ϣ;oF2j tpG^ Gcυ+62UwK+ymbda <خ1RkvӂFQLk{ZC<#f٣֗swvI'2\ 88Cbྷ=KƓL|UًGeJv|soRQ<3,|QT
=68`'Ga]_ٳK_xkğ<|ˢxTHnn9m.3'(6 W)59 3&[ixW↸ڬVvo:Ydctcc_X-Ŕ5e,n#1}x|5j?[LSfwXW'-ѵd߻'i>G߈8{MgqVjW/H_2!"iFsԍ;$Tyӽ)F. sim,YBF6w( k f|𞽠&VK_@CO]GRpy!{W~ VvFD=Rkv2P_je?OnOmCBvzt Wu֟2,yR )m?qI5NZbwZz૏5r	o_H@k
8g˾u_:g۰oA_M"4B#fACb2s  ௾'²ǿ/@b-S҄namYj(LssG3Ck{`_3
=NelssfwPo'R{'7;.2{ iTޝf_W#)v;}A  h۟39
, ߡ hsߺ
zMÈ?/_V
_"xnm7Gta}YQE!c81cT|VD'B@e/Id",$%S.6{mG ?sEᏳhniYm-#R;@$I(ӄRMngN>* h˧mfFtᑂ0 i fg	_K&}6e{(00, HۗW ~ɻlN B$~[ٟ|Ě~C-PCRJUY7kZ:uѕM#M]~}#]1XiQ|FU8Oҹ3GkiVJJ
HsZ?ிgj );Ml|C5@>eP"%N6<W?8Li_<#vKMCSs249W#M)x>F*џ2ܯQOρ-fQβXak 
~;Fq<8d}δ>~
]q  jxv!t/_-K|﹐ (Eu^%6So Suc["vjpPF|ɥtiF-y;7s=W4m,d{~QL@͟¼w 
t˧q4}&##pyZw3m
S7=UR[c+c"	vW|CşHo,}#[O)hcGcjiJgjw
?dOi<z~g,v\IkF
4AQy4 gT?w̷6Fʎ?ƾZ;ǰ+5D?t fi,G_|/
ƙyREz֚s(5+rNҾ g%߂~!|9rkLܱI	#i<m= o%lvz.4pS%-  	~LD6/lX?~}k?&|]i0xq[V-Z3ȋm^zV
F$ݷ3ԭVn	z?'w㯃(hp$o2q	Ex/ 㡯 ྨV!`9~WoCH?څzz5}y{ <nQ
7KҚ%0W߂	;G 
5waZioh?K"~֤t|5]jj*cv,7cʸC	׵mUu
o۫%[fb[y4|w6~,֏$:,Үf!L 16Egrus|/+}O7 k$g1&+ gx;vR[dcd$yp:~k_yx֛u<BB; k^N8ќ{m{In&U6s29r$}#Tgzo_|Eqpѥru4&5`nCo^Dfo%ýSǫZyh&Y, [Ah°¨i|
Kψ,ۦ~䨽WV0AXno}f3!Uɡt$eGjI^tE[N WG!Hc}EZmciO?ÏZ^cwudVVDT$ cۭ~FYfZ6\|-5J>|wTItۖ?5}Bi]:
鉗*o?cyGmn,#(TF#$ 渟؃}8#5˥EQ?͎ǽwt֑%Ԑ%F՚n
As OAwwO:ݾfm7Meۈ-O98Xهđ~n}OشmzugtQOWR!x<H O]v_~!(֦gmo,,!_LGiI1fl@L/ _,_^ |rd9ʀrXTTVms[*6vZʬv]e#_׊y
`MlL	-o˭x ?%MpMֽA7qNooi|?1UgnU\:οz4Aoc+k;ᶣ"Pӭ[Cͻ|aBl ǵhx{awkQXj:yVKA&d#$mr+ShM|Z/tkk9~&1KnPHrGx+~%^h<y}jm7Pӯ\ZhD/۴G1[*W<?m_sx]Mé<2'?Kkqss[ɄM9^[IWށX <zՍ͇xR{Lۥ @߲? fE]B_:kKdB+ܟ*FHzG/~dm'úq}aNڽ0ъnX卒gFо	g tKI[[KYK>Mg!12՚v!R\+|+Gߴ%oB,~jWq\AGIH@$0OwG/kNm[w)is㋆qjOݩ?drq݁YUܕE(t; .W<]I}|֑[HϗoHğ} >لά]C=F XB3ОE{v#]t=&Oo]*}HmY=w}k'Ou4d峅M$:9J4U?XDxO¾վ
w	sJFcyۤZ=8KY08Bo͉5;
&X>c-cDuU[&#ʵyd[v6ǽ|`|M4gX(#
gy3yQȒDLg4Lg7#mȺ\ʽsw*J7%l` +ּ13<+WQʊ^;GX^C? Rk	>c><׼/+mݤGC O3'^vs񆐹d< E+
ˢ%e +Agpz'X~*|B,77 'cV^O%}Uqj~ׂ||]4xygӚ/>wukk_ 3L&Nя#f&|vv_?դd <W?Z'!x{!Z|b6W`UflPs+¾\y n[z7c}#x{I-ýG]KCXh-uUA QXJ1ԫ/lcO|76q%Ks4e<< 9n|> xFL|aG|?^}IN2abF@sgfj%B$w~q%  =)oٳkW^#-5η
@1dgjz^ڕ.e{\ |bQ?]]x/¨b&n/gϳ[pbG~2r xOh ^CKzlHO\u%c~
h:c:6CmcXs8m}+
x=٧k,-Hr4(oԻKo-I-u}63>Z_J.оR
nጝ _ğiKB_A<-kxA!;yW'	C͕A{hPe9<=IT&X|;kn |˪<UJS`F9/O&ݴ8665,%7f
lnאE<
 ]Cc2,peA}?1;&OP8k6ҀF yǥxOvokڶm.m5=cmP޽O
SZ]Mnǭxwf~^i.2	+5VGP{kYg;_~(h\\C=B	| HtlJҦ
<GZ¾Д/M2djRMbX.+t _	K\jV{{
B9RmSz.*	)JS<	L1hU8!~~H{z>ӵK$KI<JD .H
־9j\_/߆;oyfm˥%
+9q?.^?~tMF9$Z4W;W$g	ݳ֪c}YR{g g wOԵ_ӤmVhR5*f99|᫏:kM`hZO궺k->!n$͘bHd9ߴ?_ՏIo6}
=ᱷݬ(
8{g?	㇀AL3K<Bi6W's<%N{F)4+n߄<UYx\]<sa_
kGhqO?! 	$UҿkmG&-|1ƚr~,cl[DLFf?t.x?-6_Sᯈw,|Mz>^}u>ٯwu\2jzV/PMymό,4>ӡEGWɛj[Ff9.	Z1:h~) |}<;fR@!7yI(DP6zWV{ǘN/VNqy|B漛↟
yXhy3ۍ$'#j%v͢#̴_37Eӕ.$JzgC	8Mz>hIm7Q?uv`Ok wZ~HiP/tcL~1׹cƞ's}>Mjɯ^)H aҝJi"i|+"p jcg^/T='ExƟڟ 43MgOIirc{=
.*s\Hς@$GzkwzWZxMh"7lI핊
Fvpy5TzW _닽W<M]mUŷ7~XtID'5\|*k.Ik˒-|[9&#Q$JOeޭyʧxwO|7'Hܱj'#x8iiֶ++e`rwU9 )&xǚ~xm#%z֫$_\bS
688yCW[閫y	M̱)?&/}4gExWAyMt.IYKD#b0USUi/}:PkuܗLS$~xmEX+
TcJxX)?:vݥqҾ~--bpdTko֢=]m}? ࣑c`С3+Eh\B +(qti_<k_TfJ0O\䞝4൒9t/e3ҼC
{Hṇ井ADVq_I? ri2H]@)5h[8  <TMEǤo隤rQF#meYEIr}=߿d;b ĺk	GQ$c~|	jZk@>e<J>n3J7z<3X+Gg424R.Ag 'FVw<	SeJjZfi-]6CcTe%GNāz>=|n X#d}GjkS)Ԍ׺
(4
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
>%_ͧ<,gnAt[o#׾;z"-iiM6|?} V]K+;HO,"-lFFZpF|q\oÏ[Zռ7hEHW
-w7Ϫx#~ ՙfk[V]`d^b*?3sӌ_B_N֠,V!ID6!r8>=)kE'w?ko|)k];g1͔̻Pn-Zυyo+i3*Y^XA[I?!pLNrc8'mt-G"4o	 ƹڲu=#mI?xyfب7w}RPnVT4˸-FjPTt@`o<~.i>LŊt5-	00k<W~&Fr10<	\v?\KQx/!7p±EbÀoQl_ZVk~ǧ	N3w۹٠סl`法oe.\H
88>x{sX\hzkub{Vku<吳RX2 -//
SE]>mKYnd |s^ {'<_
Yj:Xn k)=JqM)n
Ӱa&9ɚ}Ot'$#0 +	(%(%`xF?ӯ}uQ\1 bz,$}ֱF\kS9ɞqo}^Cy-کuk :Uw+| /^ XKx<d<cwvx:m&MךvNO6C+x`cھ d~ lnmG[f_|``9|Tӏ4}R>	|%u׍$CHGhT	#ymn$grN5؁8o3HXSVMͷCly K'	omkq-1%$g;W^[J**+Kqsɶg_|QOZ.V͂ed >/6b[-1*Q4EU`
7k,7A~]?
Z/mrk0ȚI_)IM¿k3$lYBб`p{~47_k0A
ƣOrvz8&Ӻϧ2->
Oi1Mok;W;4r"cVlWQI7y3oź/ؾ9u- ,ȋ{W]8V2vgo-bXK'1dsq)<c/ wm_wA
'DGz33
pÜatƿׇ~?&F-[Cϑn!R밖xg rzWh쎪Rݞ]~>>|
|y<Q6#w4o3I(Hx~0a7?x"N<TQ$b?"DD?
o< 
 ~i. KNy2qz2½z::-z<*Sf;OO>+7'Cz-$^XV?26_f_`>ouY🄵H+[w/<pnh=kcҿeDn.QH_,uU<[ m3h<͌nsJ末{H8~TH'Q7eHUե6[q@BAǽhx/
)3GVbK9MBTHgcg$=zWt/_M爼 wfYaa*c#x|x|sOFN|>QX"v8C' ANMU:4ڻ&X'bq|j_jwڹV.tҨJ^ Sf<y.ҿg[}z>Isg
\Urח~c |QY*oF48?ioh[Oxyũ̌?#[Trϭ?hρ:#Xf+ys,a26
XSwh՝]4y Ml7F>drH;4t/-wMP~Ԟ(KhM
Klʲ|> z ~.]Q;xO^y΋s.5I!dcdFrex9sdq۱&4%_(q*~*I__	~k< k]pNO0+C±~ E>F:~3|:Ֆ5kMmj6:Bէb7G@^[᦭Ro4o~hyEe/Eõq߾tNx:38N)ivgyYpd_sgd?@+ n?xPeԴxS+[Y[hX]`8W.i_O5,խA\w7~?FF4oŋdY4d 0xұS.ƘY'%go?B	-~(:meBbF}Gëqqs6I,7NwAӶ+ƚ<]jgo$~kwq<;I Cu+k5_컽HI.FVT@?tYeI #Iߚ-'Iw|,uWO2E_kxϧL¼wß/-;uby@%$8W|b-#q]3ʊ)Db69xoSכZ2Ϗvk7%n~[o#kSx;q_S0&Qs >Wm`3<~x:kS׋ R)ę nֿgh`icXA;*<KUXcGݤPіrH?zSn8Zslr_]AOW	'Oϙe# k 	(5te3*CZC  t-N`d!TL_.FKQ.fo7)Űӷ,),q_X#+j\M5u5IIq#=0C%4_Z%
y[BOC0Z~)jswobe3vְ5p 38 `Wq
֟sįXlw<U!J1KC̩:?\xV1
{4s kthVAX}>CVO[TRxvl)ѹAxÃ־U.tnKuqɵWrdr2B$+ؓ=MGfx?*4Z{X~8B= ?a?$QC;F#4{K25+oM o7G]#`=;Xvtr+
N?#Z s~]\]i <G{阞>o֢:EJwj_ pǚ忆+>FZ[nB|ChK$2WKRi%Ƨ_iryq4r:IcIx/PiX7`Ub;HTMyG翍qi7Z{LOxw.27*ھ l꺥Krm% $K89#^ C9
`	!22p	&lY*G≶>Jf:׃n#}l% ÃZfasZ.RSIhxcOߊ#ZJueT>jʎO!9`q~[IYc{GY<m%ϯ_axşŻ{
j|TvJXBn Jw
ɩE,-"BҬ?*N(sNwT;# bY>xh $/JծO׮c]}V9@G˒q~֟kZN]3:]M',FCf@9OBTYWC^OVBccƹ߄uēE e=+.*0HU m?e T汾
nUŭE}̧i^rT?ಟ~=i'Xk+VP	^mJ
RqЌ |: 8Yc9pQI`|YY_?lZ?&u	Dn&I,C9=)3WF,/xC Sw~
9Xv);Hv,2q^x55W7.yox\;!tּ`F x_  ğ\_|A$ ]r./Lr;g߆߰iEº;F}y#6\ɟQ#fmSA](Mv^gqj~U\x:>#x'Ro<)?/O%d*QI̛ ?fxkxvG70*&L~(|W hqPE'.n$ ~Gt/Gئ}[AKwiEb=xrG9T h??\\\<p }pҶZ%'vW hO-_:EvӤ,p,Iq?k|:iM|xmdpvX4PO$4Ug[ws|ֻgwY]؏ Lw׊nrVInbp
f_-,aԡҼ{&j@XTj#k rQ_v~c\gdc'*¾dΏ?uIbZ9\4=poC>gH}6ȉ#Rdu}]189{Ww-%ˬZ<N"t»:ZXUV '1C׹+H~\7Iako1O#!KΡ@մ`Fz7"o؛rhzzkY`ģ^w!G(aEvc^]xT?k^[~#,&-ddm	o><#5?I=j_x>\|[Z e
6A9:Wbi5zrw-~+(̓wIO֭|}[~_: k<Ha ~6_R	%^ֵ34G(Ba9Xsq<Q 	+~|f^<]kZZ=2 6G9>R*N9e>~|E>e|AlZnnpt)1^< 4MuOm|){ָlaOKE߇4=B]kN4r+A1<]Qk)xkKVGSh/Qg$dbh`uj;rlm%nxA|S'8ʍk8-щR-V$<`L_'}Qdפ.&ί-䇐=d7wƽ/G D,nIcC#qPRsW^[oIy[8o$qӃ=#V-Wg>#鴒G澏~uxe_K'ِl|m51}xnevT䐶0qҿϊ,xmtku6U;$Wv|k9Ɓh;y^@|B rprq\>i-Ίcwfp qznX`XKMQẓ&VzTZUYYZFv4RFUՇH=B46c_~0[/!K 6h}#^Yn>pbxq"p}Ey ߶YlG{WU?:$_Q~Zmt['J8k}Oz
2#u%f|s>Cԉ_8X)l$>><wG-j)=ca$$ =/ ?
^#p@WڟxIYOPp|ϧʪ$ 88LlN1|!~.ySQY_B	+mGg}o6xe)oi=NQ?*<5|@ZmzмS]
ld8W)Ҽ{{9<
S_Ӵַi$S[.7G f<ֲM$v&z:4~/mBK=GJt4!+n8l$=$_ i7Vɥٷoy6N3i1:zLo~QcY4nǙ{$(t?qwBH"hw)cGϝ[-u7nrIv>_^I|QmGK|dprK
h?1ܣnxW◇~|Amkş^Q+~13;U<:k^/jVI%<Hg\~['Ix׵8ǥ-;OG_oxW0}hzZd[$>H<?:z?ssIq-$'[ȃjX G¿	/CmoJs۞Osߴ'߇	h\$1wm#GC]\.Xia
Ԭ箯p~?<gkZ߇Z-ln-+±Ms)'\TI,
Z ?YWşxΞ] n&p>Q+	uO* pƮy>_?+$'ul6חO
x	)J/\k;Cwu$34	3#3rNqڽM5Yf>!M@=Jkj'snSoCČz|cMzZ"N,hBr tq05餘.;Xgup64LG>AAOqZS*ǱELu MBX'\éú:B35%r8ӱɴۯ %hcV7溙Xo-,HLdeSW%z [կ~(GSc^3kڅ}Zmr ֮s*n.-<եk8 nn-%e'kI  cu澅{k^;^ce񭤊}hFEXKdW~Ѻşh׃Ua]Śņs
h
2J,E\FIU6bĞ9i"x ׍]kZt8I@
"ݢ#WTt_>&xm4ȡ9M>9FS*gտn߆G'x}5丂H-|l@y.esJĮzV dCtu#ԭMR3hW.zaUyX񞋠iZ~g' ;#VͫøG=c*5D"8?kiֲx_¿5ks}CY`k1IC6nx_uƩ<e5𝅖b](i#<V׍t(~/<߼><|r b;I9,h$/xBv0yrx%x߈ d++N~+KԾYAo9cR{]?:/+
lor=y(0rq'8?x,t=?W,[~m-s4;]G#+|M׵x~Zy@.M(@`毖v>ifM?HB;'ܗݵUS^o?e GoEN3mnj?~_R&S&Gk8\Xs xqn>O|+{+ˢ.8xF4lĮf]LOVO&P	2$G7k|b|=#l[sX8 {=࿄݊~=g۟f,# AMzƑy:ď
2= )P*x9t3槻g{jM#7qEF#F3c_N |?xK8I~yۀ-t?Gk,vKl_#F6$rާ?bߋ<;g_◆"N>뚟ս&XK~0Eut}7V9r$twP	iR1x	#E<;v	KycE=ھWumC^73H].x䑉-B_x@uZrߥt,d#c~A yMnE@T@J/~|V3]x6(?}KΙGX;1zWԞ" ;Eǚ~M2P ~`j-cxX"<ۘ` z;lU&8wQQ~6^j __\᧹ٯ
:3;
3_7OXnt[uzLWߴ] I?n%Fڌ^mU V{zɿQ5<CF9M'KVf# wgO0VJ(\>7uoa"h[}
x`zסߴOoZDWZO鶶q {Oݮj"]SRP.-2M#AbYfa}[}b(VGT[>mנ׼ibQH/5aMF#߷ p+ŭͥkfhd'Ks_p(,/375 r?TW 1?WOWNE/J+;((((((((((((((((((((((((((((((((((((((((((((("nijٗ×~r?JN㊻Ux^7kķiz.G [^h^B'ĩ噤v$c5*#o>2JԤu%Tn1^gsh?2|k2cSPʿk	|O/^"|MgVUԴmF,KY [H@O;Wu2ZAr@Lc tL3.hm~ gZjf`˒KƸ}|or22W8=/7|Y-Ɠm7ٮEoc%X2\((3&֏ggM
ǭN\[.AݭOouScqu}sk JvĢ;`>wh2i6e6CʹmiQzFCs)?xnSB1H]r ]s(5xK
?Mq
6_o.!Pr2T*_)`Rk_UB$xW?j.({sGkkt(e'*!eʈd͞A֖>复- -w9"'{夔3[n S_CRW\5m{WZƩ@;!R?w(a rco'y/?`+^ZOi +MFq#<rç9M]yX6>"NKȗOl*^ͽuj_?&?+t/籒6n0;ԑ]ǈ~	j5mu87Rں.e`}%_J_hR7v(=nqTU*Ng(={}K/C{m	IѶw$yBZX <=7gSBP¿?`2^o<Y%4ԋ3Bqx}k}JW4Q=kь~)Jp'woMx8?Luh|1BGA
}C^7]*2\Evc+ȬO_Jφ,D>2-VFTԞ'0pcU< {֜rLVqTזZ w	Uwb2\ |7ŖV:%_
Yd-[ht.m
[+F '}q\/x{/+J4XY@UXK RޮG|1wH^f DJ4Ӎǌm|s
)R-n<
a9K)dmT_i83> } u6s{yJFgacAXg5s?rkGvf*<0BYHa^^:R[j|ksŞ2ƿu{K8u+HoC<`u듃L_ugk\/%9#]J|Iq7ھ.j1ϧ fFm	gZ}m0gѴ:8rW_WK]_wizwQ^E"\ZAt<dr7`
K4vfnmAR>Ov'6bT:ʛeRg_`T z#}7~_|3%gjiuXͶKaemŤs9˓_!?>`]J8ƻuhMs`mӬ%_Ǿif7SfѼOouO	|R񢴞!JKj-j8K8ܣ>GH WWy%ݮ?~(izV]ctdc\Clȥzt]=62ˁ +^~uWz)kSL>O~SY n}sg>dVA-j
ܫ2' 
kC]t
j[ӗPlw.t`Fx O渿%(̳ ]T Z3d("askp&o,^~Qzsk_if3E=Q\<= h=zYSqO!zjGuWNӠmNL'_5oV1|7so
~*"c͐H##6 ZJp@1n~gc|q>>;x2Jg_ ŋt_%|/@K5ܣsRO4/7r>oPq੒ Jyx?WkZ|\o5[[kvkx|9F\m
#=+σ:WsŒi~+q}.嵖XP@2snNx*_N.
Vw4qM%z3wko+7uim7$?o^|'?i7ޓ$z|6vBՅja-p9&X
gZLӕbC&օrnpALl3Iv'z>u^=kwxZh[扆6iQG]ŔjşSˏEiK,7muuy:WGF$V^4I=ha

pF`_ٿlG5B^&T/+ ֝J/cRMg}|c߇zoL]L]Myɩ1c#K:_گo>[ᆷ໋}f]/SZ5{#32l@+/lx	$R@{.O\t{GHVV|2 n,ykg(s+zG3|7ERSx~
KB1-&%UT܅x n[^{&=KXFoBͬ9ie7gf73zWß woj6IwyIHfj0[_OO_ ^G4Ts9ծmXY*2#D6w0 1T+ynd	hHYBGC_?ZXA-ęڑ)c}M~|J;jzl^tī
H<]MPA)IQb#HC<N'8x/^~kBI/[Mb@$*ʄ4#f8tgQJWC'uk[ϳ136FG~|㏃̰ņp۳a6Ax-#,g}W |K}oGKZֶFs%۞9Q]5z?-+\@xOЯ-Dp2e'*ȯOBգ9 Y{Le	A}Mw=sz}|R!5;8<X#QEfP	~|A ~>M.5?
xѼG;wyy*H%n7#Yᾃzb"I.byfW1PF89-9S{1kkOB6?\jcQG.gīW$S!&# |B'W?:BI\2kKfM۲D$ѠRsdp9#=TAͿ2J8}Ҋ}ԓO~߲ωWM>J[utAn<*nس681A xƟ-Cˢ#dbھYIWRGDWcSg1ڣ<.TqҿG>!Y_׏cf9^v}3<g/&N s^ |NBR^"Hglfe;
%?zKΏsu<,[W/d~7m3~)Ś&iږAʌ9TG,잵?S|x?\,վmڏ٥raYxߏ:vKaiKN_(<Fvx H+YUvqƌYI?S*Ku_ǅ,oDs,%qZ_5 uL!InsҼw|U4hn-KrXp~e 
%fvc"Tp2ұ&F؊~V>-?hSZVRO7_Z߳	Vp\ZwCUuL>l*Sog
q~Z~oZ0XXNM4q+?W?b/SCx'+m
SZzUg,.Jw ¿9 ^
o6AyQğwwI}ut"yc2d(P96ߵ7 ~.WǦ_ɟvzKm>^К3⪶7C+?CIh?}q"\ׅ4U;O d`Vؗ#I·^[JxnPs.6y<;K4
\ 8unm2F_`n!^x?QE歭躶ծ4K0">U PUIgUC> mO#7&fK{k64e<̀E.	1Ͼk?xnYӾQ]+FUC-Q8pOESPco3,RI4%oO8rlsjYJ1V'ό_-f~!-oc4?6}
!CZƊ[U[*n~.'E`9#'=͏xE<WNbŵî_d@AGm>~8ğg»[=A=߇KAĖ_k(L3dn~]RkѦ??fM.(!>%nuUE,I8N6E:kk)N>ާ;&5:vZGZkV,HnN⣑!\d[eshz_$c^x0* <9~[ SxAIXnOr%Kzo	s?I&kkvD~ueLL?3}w-环3^>(Z"(䐟6d^|]Ǩ_4ͨ_.sg]\y'QUĲHU+< ]Ǩ<3{FLP,FW3>Gz';OjZMޡkh⿕'珗:DGu.x3]Gͣ|;3;6g>&fBH&A7|J:O yuqco{udәI]w0 }+_$$.A$$F:% q^7CVUk/z@-USih(Xg.xGeC
:
	dP-~C9>Ns|z}jݬ>mGRB^F/2FF<W3|p^c*Kݣ}4!C~P{tw=}]Cw y@GxS¥nd|m; u+mWɵ-^ZKۧ6 џ"==W=:wW]^&𞇫im.q&sl
ec.N1Ӷ=yOx?i1mukaƶQLc33&4z-sos5/~]-èhpb7 }7i$UXT3W~S|/}ROn՞KM3n$24.$$1<{&QDqΓ\$yH$#/Ɩ>[KK׵Uemf$gH3׹|.T⾋|6axoUXy,p&H_b J>T8#rM:ɫ+
~Ǔ%\{[85MEǃ<.d 9IdW=(O5kD_<_>+xZDaKxDe*FQz>jƿ@Işh5=bP.$ TtPIݻ'{#Mn/$m?Tj+ylzvƫ9Ͻr [~?~*.Umtױ,<C#=^1oAտdOxZ{H^H%Rc9J1;u5_Y֨J,i	c!"SaN[! r7 YKzsq#m2FyE/t@F.Z_i]?NōLLeg` 9q_[Yڳh
u5kv<׉||s#Ǻ}}mg1ܵITJĕQ{eΗ=esYh}?y>'[֔"Qd#En< p:b _VjL|Ao3qH=8x>?L˚m/wBJ$1OP8Q CEѾ>Ath-t?&frKz5[)+(J־ |b=x{vt;ϙD;e.c*j> QTֵmCZ&Kwy(Y7J3 p   z\𷁼?x;'J / 
*#2N5_OQok+}
8${tiTiwfQJV9~/
yvכxMnm۵	f]R@_һnl)[~~{/[Kqs)yHxٍXʎ:Hʖ%Y~q	{bnLf_Ƣ@}[iA{Vr6GqY+?I	OgL A'{fAΟxG;k#6iLh@If}Aaֺٟ_\m&T?V6xDZJM;0#oQ_QRRXuLp4yE|To~I<CNѝlVF;@ ß<k{7EjKe$E7Xڃ3_a|T3?cIl{r,>hRI:ff|>ɮmiHCy2p_{W)ˬ[]xOҬ繏N[_5VY%v8w~^4o3uuvLkvE#ȤsD(xJ|EquXAu	ITHֳL|_|ZwuP?_As5AY՜$(.ۓ&8v8(⮚G~Ӵ_	[ivzz0Gn2Z=~?
+<FdY]W+KGW}6;rT@1`r#^[{[|7ּY>ďK:ڦg>@,` k8<_ciVr,S{V[]H.4]'
%
"3qn>cRզjikgytCii$QxQ`/xWѓsqI$9"JrSxsX>+_,wzpiWcIڸcӕJ6܈T;;~'Қo|G|Q&|#:Eլk6|TrK"$OҼ^>Oƺn|V<Ai)E`t3,PYBGkme_{,zy;\3Hc|Y8\}@4
DR:O+9V*ͩA'w'xk߄6֯-n,,.AáZq,I0xbcr Q>0x%Լ'Z"]/@TԴvIGs~%r`:wM$MGRR	@*?#K
|#X.Ŝvgw4u(~##^CLx8MSYKI%`!
变 0\gxgÿOץˉՉB3?Z&-[ǿ;PYddBD֣Msþ^uʌf~<JMlr~OVe
0(,#s ~;S y į\׮'drֺzF#ȖsՁVKOTX>Ry7v݌ϥo=H_q{Y]*I@.zCkhr)6hVc	,"H\\|j|s?Iek]AjDU%^s_C~׿ec /Boo	]b
ě{5"RI4ZSwE_ºEǋ5_kCԵY
oA𕹑d=1_A__
kWuIf$\ŝ}os>^i֛tmZfV)8¾?R⇆u;RUP|<>zxk⦵~(#OI"ɘb.,zRJ@)JeǍ<5VH`d10zc۵y-e.o1W'? > WMSH֗ZkjYnV˻0x^1
潮#r$r.<˖Fpyh6-xVVw/ŽC$fO
Z/MӷO
?j.qͦx.9dݑE1E+|ؾcm嘵x23H׼;iEw%ǈ/V o'Unrqc :H RWĭko>/5+x+A/@+		H

F3/0,R=L>R/JZ@( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( *n&UG7~ê۹ɩ̨~ ?я׈uv	<1gO_]2{ַO|n$>{iͻ#<A:
/"|Rk9%"X݂RH {xxL	(𔈀U
9\LЗg,| ,
}
OUaۭie$03^9/
z3*B}b8`!u|y(M+MxcI"">5{(c'}I\~ xXtlVמ @kij`enaR%h qn	z:_?L~?<j-"""+`#(o|<h|/Um0l]C<ܓ:5~_?5χZεise}Kesκexć  \~8|?}jkV+n|9F2{cڴ(Wzo^(u3ēx6zO/5Vy TeFk#&"kn-KMICK{;xWTI`/&/ƱfE񾼺N;iܷbm3¾I] \1x+'=5-nk,-*i+m |;oo?<mW%E@+6Iq[ZmN-U]Y<1	/u\-ޗD|5=
 7u
@ƛ^ڼqHyKǀLݰ+x/'<% >]Y@[UFx8S5=EӼ!L9LʐAqy = ?)!#
m;R<@3/k--OHP̚+Β.7}eT\K-ƿ	7O^oXM݌3){|¡wm$n5_K¿>:L3˷=+??>?ci0\Z-ŋD[Kk2:6_4 >_>X,EZPbFe2rNErUQV=
5?rNSR/Ӻ<Օmyrѫ2 9=+]~?ϋ?h^mG{oodxPKǽ~&TS9?6=֬ugا:7©D21"@r9G?Bxc^x	Zx±h/.yAƬR|3_Y玉KrM%QmM?h?}s&	C}h;{FvpzT:Otu=SM،1; ,y=t|_~T-̺4鯭^;V?g\F'@	QşՀӴ/	KȯV.E  jI%/ą͹G?E4oۯ>EVj~|ErֶxJep ~?1V!<ק	|n{~1Ӹ>~}
c#=P?J>M#	H7k5Sď	$  ZH'죎	Ute	FYpH5qW$~|\3cٯtxgY쪪wM|%iru,M ,?Uy_
>-Z/5͗R-_u3p2mg aW t_
vey6/SU}Sn^$$+2"P\ߜp6(jeBmɵfmw'fh~h?n*\G$aCr>Lu2 Ծ/MgZ͜D<sW?	?m_Uo/
sIhbm-ͬ~rWmx24?Ě+kV}.ZjVF@b.FʌkJBJJM.Y~|>Vmcjd+GR6z w5Ɖ6sbWt+( )B0+RM~8JA W;y [lŚ(O(RƵRVPqt?9-揯G
<zE4t$'0񤟴)-
7OĖkqmwqq9c%1lF@POS_V5Z[-t;}WX.r$ҟi&  .8y, /i^
w:":F0	 ;W);SУ哺)
wMˎWPȳ3$@
AtjOګ]x\g溼B:bן|.~뷚\i7RFm:Y|ݬ9~ #Y+'t[F-yw3c
Τ`2F[rɴعb{EF[Z}=e !7\Kn,[YTՕ) q\o 	 Y:\w2i,I.VVt_ |	^KW_j县kcb-f4;HbXɐfS\$gعA%ܓz_Cտnv|{w}dCsoira\_%|+xog-isoGWp$3]Ãu
6%%0HdCyv:/!	CZ4<Co~όQ/ń0fNXڣs|dMhm>C¶
2	K<ew6%#$
OQG᝙-RSF}a?M% - i#ğ t}7VtGx
2J9sg\z?_XtbO
fd
ncyoں10e_ LQssxVr(FFTy+¿=k\o4_MxzI,]5mwG4v @9p?">y~Oo򴬏 =~[ f |^-XxvQh[[.l&C5$lwrU?`xN4j^PfuzM]mm-DqBncv-1'8=	YtsӔi 
IU\;[,036GuxmGcCfZlaH<hQ S/#_|zO¿O@)-H.14MtDwTP n<_63<uZÚah]UṔl^F,ٙ	cAX4*IۖJ^,iƏm{oPnT UWon;6iy߀?࠿Ə蚵ͮbtȯnՖF3:<mq =r-/~@Ȧ쵛iْÌ`m/;NM+S7ƚ"X~>8+5ns|}}'^Ҽ`5'KԬ'ڭa2	5*׶|Fu_|{5oK]v7U	UY~uc&kլ~.%F%U2x9HTA IIvQ $ )~O~J+KIFҠ($`wQ?t.mYRs*-܎ۓgX	@}s@7s0cc"+5>%Q;ǱUփ$WICۖOqI#	a}
4)7~LW
4fV+n7"J۟*:OR<f~O G ~8t}BG
'cd
ct
5~< x^_Qdf))8
rlE*v7x}(~.no}~u7mGxJ\L1 ?ZCo..mB9E (R"(=2qԓO?ߍ:.sq$6
y=f+3:T2O9iRqG "=&H[`]󞸯 M|ό<yi<t(_S5n<GM݈g c#$|Jփ~Cޭ
..m6myF
Jn9#kwp>e:n(qosCB@p<;upVqԜU]3sG
Z4ruF}N{kq2ʒ`0J) k OO\6kU[L2ʞ{߂'G5q9;6DP;PHf6y^ys~_	˧~kku˭OJa@K<D(yTfWK;O'?oֽe3īܨmx'+b~/3BϦ%l9z}jZ uY,w%.M;Bpo{*g.h?x.=0k/ml ILY+ŴVK eDy}6~ekߛC|?_~!WIv7	wi*[.Ǹ[?__ 4Uu!j$$ɘu]2Br8 f'>x2=+_5տj~	5h\w.{F ׷_QkrЭ5
>#N5@p.paWUz-ҪOٲmMdxuF0*R	
,ד_^FLv^vQ
8_XXs$㽐^Nk~d~.x.⏂>	ޱure&$
АS ben\𦉧_k~WUm}],6l^ٕH *)a5s+sJKSێ#ܮ<÷i(㸲`e20=зM $0s\틦h|eC3[ʺ.0n YjwTV~IYKA;v[f5ɻ$3{ᶡokyմB/-e[]ql\+esS}qق(EǺk8OLFAhYbO#4
4C'mJUcqc |i5եǠ]̑Ym	\-vO6^C"Ht܌&=kiڌ>/Qɳ$PXw1#0E 5x9BxNr>\\ƽ3޽_E*-+|Z;5/sxv*{EBr0{zWZ?d	]kTLxsgm,ԉ,9G~U#{eؼz<4r3(Bttg$8> o>-hiUs9mE$ yI$o +|U M5-A4 -UxKs+o+7jaA~?&gut%I[bmEUO
7'ښwF> gi;x\i7'JPT@;QDlxmFhz4kɯMGZt0єy2gCǿ<n>g.}yK̱	s(u%@'<jM co	Z\FdP!y᛿sJ51H7'w+|'/ٿ^,]jZ?HЬu-W|<q,3  B3xOƼ4kVӮ.5(3
2fтG>o[	1q7ZSj[t;yW(==*-H㾇umsY'P 5u1jIFN9i-[ m~:]^bKAe{ʀp3yt/:ǎtx㇏/#֚еzM.^Zdg*Nد ix^_x7M$^i}q_JڋPF|7q*1eǒ{V|'&tFN;.gmnʭO<H+^M'=+Uxץ]}_]kiq隆ym tl,vFUq%<!xQ':<EKD^Xdg9%5|Lw/]MWx#	Z"ok4ڝʮ	Xے1]Wu/<I |gkǭ#q	lj}B0۹)Q(|Fi\^B֐$uwL9)g?ࠚK蟳.
bE#Rq࿄t)4lD+l6F4}1&C&FY~y_WWxM޽ͮmDA7b	ǦG*q5SxvvjzIi<y7S$|c-#1ӵW嗇<ejvLSEK`>$
S~|mo__?E_KPD)< u_O&ߎN.5RT"VRΎrZݸ29ۂj~sSݞ@/xG>!|+^4;α&r$07Ax gę+ņ)KöNh|^k|<Ε
|<u[edѷ"3e8S8u]&Ἠ2Ӑ#]jrcNܛ%xo~vZOn	
s*>NHPO5 w˵*Zgehr~Kqt'zCa|?oy]Y4Jyza5A{h#00t $КkMlPl>+ A[d5I?R[Xgf 滯dFVM$wO;8YWݚωvS~wqNֽK۫$ktsA6 qc1nl:rѥ fizq&kK{Y_rzזx׉M&0YIA>W'[6w<2ϝܳeN[8018]>Wo&>-1mm
^Iܞ+n\t
pL7W@*̤8A?ci~7iuԼ7<u_xz&2|qc}w6LkW`^|2¿~%kV$[oۡU
26<ǜzT2К|*+V xA15f|̫ܝFz[,ֵ_Ey3rKsּI |`/xO?#	]5v-qM!2qFHwC
DjΟύ&WIԭaĐI%q$(EzҩAٳG# f=sDzį~{M}v5ą#;,ӟuo5Y[\Ox~Z7BYv B'wϥ|uxO\ƽG}j
i:nvg/'1cֻ+?4ό~m tkdaU,Wi=O$գGR-o(/<a{q7|}-20sߏ->%xzV-NXC#f9PDI2BM+KQYnNI f/z2f$דl1!W8E=q5VpQҥJMOSu67ÿNWX
e#,ņII<jK}*kX8_-zݎ橬YgCxSѣcH*:>z'^?|xs̻ˈ<!Ux=+Q:7S-A,؆8GX$o5uk?U
ZQ)m-V\?ׅn4O|'֬41YQd/cqைr¾UZxM;\'\d]"gMweS-x[_Z{St{h/M#16\ƫ/3~:5k(QR@7_+ڧ/PLʡ:o	pN;֟?e_hɆ3Iow
ԤDFT fAcS>h4qROЎaBNH
H>|sz><m.{[95C1h=Ӽ|6N|
JcrX,-jXh{T/JH-aaub3HЃut9?.>.׋/aŧk6cca@Ƿ0}C>ήG3\][@lM"炇_]]I8`ebm-3:1GA#/t+|Ai;3( (r,F.	2%<I O$lV)ZBwccQZ
o>Ũ_Ftu3ܟOk&LWa#ksղs+ŷwA
%;x ׵c,e*RՙJX@|m=9×CW#Zk;y&R0+Ҽ-WGs+߳Uύnn	 [+oɮ .@YbuǭO4^+|r 	9+WIx^jE[AtӘ#{R0xTEPoWZE/icG
K2,v3 g+\?o3MMO
U+xcۑ]w-xĠ3[hSD Z|yW;霏AaҲ:e?|y}>Cnmoj8
y~+Z_xX5-jyc
eُ,8k>
|}uU|piF#xg8Nƴ"	xu -đ,VK"z/|xC^V"0L+?4]Sdz>jN5ʪNi$p2N95jvZվx7rj΋qky{?Fܪ
᱂9kI6xόbMÖPq
NzO+^2hB[F
lc'` ,r0GN+6OLDB8$&!$c.70@8+mzJ >sLN9|l{Qqo#㨤_[Eԗ_fvrNlWe0ZpH8_aHR?AN2&U~#B(sP( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( mVX_LjJ(/?MOP֧.fd)2Hqs2YɮMCK7#Þ1"#50>h?M*=
9Zm=~L~˟?fZ楪h XGϸ3[AW
+erXcsYw퉨xvԖ6V[X,f%~ml [o'/Dy<	?.Gpӱ ׉p\iiLϝI$DH]Upr1ٶT絥wϦ?< o"Va-&(nU/-VM	&Bïs
?QNF9|3e2̧Wÿ`vNY_Kuia],u>k" ʺ/b.R# תϤN-ܛgm
پnO?|1V jX;kױ~7u<{oj> vTԺC n?vk'lvmty<	__~>폊|7'.9rxov{%ү?{2Jn|x5Η\Z>byB˶cwnhyy]Z=𯃵(X[{5%QD$	`
p1_3 \16T#,v-4d7Q!E<;g k{ |w"C Eccp0DBOӾxJ?iZSF[ZB|I#(98k[JMQntFZM}&W0n\ NUuX௺i+];Ko}Ctֿ0-`,edo-sB?

񝚔m\6jyHqyui~18 _TǾ,쉯GZֳjTw=`ba_~$M2-1{_[S7ln5	DQZfytF*zҺkQr{; 犼SVk⏊ZY|Ow,r]~Xˎ:W՞> |@ү/k6qoN1",,J?	'csy?KRKye6^6S NwW?<`tsz
c*6eb%ܒ>4#kox\O\.^	Dxd_B2BZ^m
z}1.̜:8LmV a.ݾXG@c'5-_ږcZ^E]@FtVܤ0܃+iՍ%p.W$W>OkzM日+JH[}&,2yR
m2xW׉4#֭4mZ+o&"mjTk<ŎS"mQ 
7׌>x6ݥߨ M@N-\
گo7O|32PD NV Uysc$A;ucX+%F1/&w(!*@uH < 퉯%Ŭ3<eaHϝҽh4ߏzoxEV?\6ˢ;"'$/Zgi}Qxڕ՞Ekto m)Ti鮆~:y'ׅlv?>"xhzGd ђo'qBNI!|vOh7<⥻Hh|cᦎyuRqwˁמ?j%5^xoP:Ng<=HaZ#!i-.-m60g Ꮧ5<EH6&mR9Ri^ƿ'G&_7uox
[M\$I.KnHP9o	K֯4Yئxȏ{b@8VQ*r?Jۼ|LI^~gschƻORfewk<qI
[zV<(ȯ7u
nBv>\o
Mf<΃Ǡjx^ OmbKa#TJ_
uk TxokSC+F:dQr&{pT.g> [3鶷{poHNc^N:W2/
Fg@~
 >(F$úiw5-K9l(CioP_x_vLmiȪI0w?ӽTpFRE#b_2U>vA^zױ|9(x77ntlHfsn-h`k
ODq'MF[ikTY~lH"Xg;Ӗ_T_Z@xO^еorY۬9G	rȰJ?rvGN4ᯈŢ~\dI<bP1?;[PI|v
@Ȇ7SO{5` Q<v{O\[ˢϵqԄiךkK7{cBƎmNd9'ݩ3UkߴO#{yrDїV8^F@]~59c/ZGk{qip[+쐰nt^9/|;7kv" ~~y{W3ңZ>BCo:kϊZլtԴbRJxy#}a
6 qC# IZk?¶\!GmR*pHϘaڽ3I =]\Z$$W2f9RIVC3מJRJ1>kNi>fY\}j"-$RK˵I%Ol~[|K'Z5=WFӮ6-"y%]ݗi9d]n_ׄ!<1Y|Wmڽsps=*ai7M{G*7׋|E?ob<̍<A|>K?LSBL;ݞ=}k?oy>#\ZE&o6MIYe?DzNdmry/LsOǘ֤y]SGeE썵X\U}͘`
܇5wZxZXM,=88ןSk+xHg	,2d?J?-7Ԃj`~WmrU99'>Կeteաege?Cz;Ki1]~s_!xw[0w`r?xφ^%X<9t|]؋W?K :XzsVh^Ҥw6W%𦟮b7i G Jɖe%-7ˉo~FXTFG=;WoxnYu5c lߥvs\7
!r)IߔgᏀYqڇ	wSz	:P<?/4Xuoj[o^IvUZ w̰rW⹟25c%ōp&B0q hWB.V`z3&[*-M^ƫg ,r1坹zT?d$T[6877
9:
hN趰eZ}VѻePsWݵ]jMԡx3e9>gL\QΏ*ퟞ"PPiZ{OH噣MrJ ༣atL5dOxFtI4]inZWY `
8 W g>1ok%ԚJyrmkz8yBmZ-Y"WTi{e
@$㹯׏ G'r+)R096^ ~:x,,ú4F6>IIg\|6 ,x^-O6,lFiNĕŪFt<7O\|̏ڲ<n_?4~8]V-K~Xp ޽o_؃es_|vkwEF6XSޯNEKhR<|i>:j 9 MðŨ]#wϞOӮ+D75)Z"EJ9-03 E%W+]C734Ѥ0H.UMN	3fP
_
&/ڟ«M{x8X?Zv
zTc\ ÿO]gN
WMUh2Yks$Q,(P@3^ٟU/[CᅸUUA#H9׊(¿>G\}>5/8k|lgAhd0xkD=,U*s߰fK?x~&Fա+{;8f-d'tH9e p mo/ma4y_MH쥉73ĥ1xc
+6|2CYJe`C;nT2fi:;`g5RљӇ]hI(ucķ6&'w*>vn?/YoI h/#XdgY+<^8q~=o-m	5q -C6ݜ|BYdYܿ$=E}&C'*R<?95'/xZݝʩnTv7?7'?<G&d|<#\jƹX nk 8*fTLW~vgz{{5Iiz5MH X'}:wV</M.:<AXn6xxXIލ?|3m>)} buX'=}׿|'<}ox)H*iC6N# ߨo5 jڶ-.MymZq:;P|[rHv
#KsPs0],[٠i#pÍ!^[Zw67+m#PUTQcfn<Qc"Wl|FO+Ƿn{w|oqx~zm_|ZA6hNߔ f| Q<{xEZyƧF_f
l ~k5'S&?6
CEMkqHd#㈆zwO[ ZxcP~Z}j6Y淪y\.՞"Io5jsJ+* 	F+{-3r ^uY9=>KkIh22on	Vrn;
fOZמ3\xHUW#nQ#NT+wAxY<QxP0 }cP{|澊F[ v=	-.C*XXgھd-8NޟݡgQYk/߳xY-R14r$	! &+E`O?kMxFivey\#NTo*YqY??K>Nڦ^c²\v{`/^;^x-=$5m/ZfB h5Bp: 7t?i?yhgSoS寈_5?|e/x埇ƥK5ND!{H<;OhqǤio $6I.iqkʪ>nve?*bSM-)% ֳI{EsG<~d}
@
<E3hQ}
Ϳe.c}D0.}>Py>#jl?--Jc b[Oz`
t GsO<;MkZ֖]--lɹWJ4*`ܑ{=Ii'7,vs~PjB}SAѾaq$Ac}knX85։=N᠛V'd|nC*}T^AZGkǆ|y߇~:.2jZWv$3.c5Cm-:<7r%Dm6=܈+?߸=;η'Po#fmg%^6S G?!A2ubs9qr+4_ڇ64-sO$7ڪI,urNG_ u;OL!GwlNܗ"!xOR==+9V4mZucvFWxGSEhfXܡ5 m?A^ᫎ^N9+}q!|I/<U5kQ"71^,@>fK]B}8^^qwv@Uw" ^ݏ\|'%n6X%ǈ h~ޝNm9Y1*lP;ǚgAԐ-c"S+<q'sMl㵴W5<Eɮnbfյ	l@B̀M>L6^rhQ
A^ϵ}o/KE,u$#7%FvJgg$r?ve
۴{vwnwpOڼ7?<GvZM|ulM}!ᔿc&.,?j&K7bpm}ׄRUvqVMk^.z9I6gf;:VD]|PSѫ~⋫-z*$~X75VڣO
2s ~~߆^:6,Ce狵Ht<##K$YfEaxs w?y,5Jz7\Iw'0$r~*_ZZ\gFҭ
֬Z$
fg(Ñ5G/Dꚦw#ȘXe6j򿄿މ~.Okfiu]NiH(pX	bo?m>ۆX	>ʊwn#_]EOSZ.-IIp%rakf*U3⼷> ^|sƉus,ZձJ!Yi Ui
iyz|_dG9V6C %<?YCW qWeRtE45:S>^fh../gyfXfrH}s]t>E!rY줊H؁2ݲ?*>oVg<zHo5xfGKy/3c1R|NF<:CX"G.E hni]>+''7[p<3Wl1<
4-8вZG XP|D𧈴F4l.J;|< yt~TfqTϹß(Qi4RnHK'˝u_ve>CutP6^P55Uݟ^E&Z ~wʼۜҿ!Z칩|MIm/.4h-]:"O-	9G ?/գA `	<()?+t [5oLqW}~:ZŌ(ȹ;|S@C/xTSIFs<S 
ơ=.g$[<FFHFTɭ&L.4H/c.a!;@zߌ,13*2CѺwtWz#E"%5
`2 hEilTq);On Q;=x(譴~>q& `.Vk?h:,K+PO8~,ž$!tiF8j ^xaE׏<gsqn+K.3 Lex5ncJxQKZ<Jaּ7,i{qGn|u;>. Achc迩-mbX|#SfmjęawE1vFk⟈&L6Ӎ>͗pʘm&1sUIQcsIƫv=N|;=X{WK~wlY|YISױ"AHHu%mpd f:_7 $k܋HnwdͺʎЉ|Q@x:6[J>YbZ(R	8Z21]>X\ZG7<ӡ1?ÿ	1V\e7W' LI>"uF?-_\m4\Dwkdk*m{cӠ.I<cyXsuMiNo-
94c$~q叾cr?2l1Ễ[ƩH$j]gܨs/"^/5xd!N-9inc
ZIq
$l~H~N>Τ&8;#ӬC x iׄTXKdF$(|-Hhmk8(Q_õu9|'ph:NwAtbE ;1  >I><EtuE(-M^drc%JZ1䮴?^ pc%x;C<EC<4%*	n2+χ\<viwKo=f:a7yu
~i.nW-˳dw
vW8,}>ԡFnGbV	$B๿>h]syzhS7ҽS7ǆ6z4v#c޿6>+X\]:	)e!['Z?YoZW1@O%]p܅*:<PdI3J0e9S `rmwR-̍$趥|J]jQE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE Gwڭ ~J v`sg
IՕk+\n,
vLac#5U-6-NH)EEܬ=\xtޞf+]?Z>Vּ=egjdP$'$Opq
Oh l/$|#g43Fu ׸~ E-PPOLQXt$G2t:E|[f<>"O>t:eLѝHVʐf9ekF&x77⎵kPoЯ3C&Ȭ
0U!:d,X5FjDG0h+i6T[1P2dA Z}*^ZRՠtx,s:{׃u_0/Rmg$ry 8y:֊݅rOs쏋l/B|j6}N?bHo*AX".kt
Au߉WXܥ	wvgoʲgk>&fC$Q ;B6
t=U\+̏[۷BWs^lw<@n,nxhOz7c'+qRjakyel3 ]=?_u?ƚ߃toF6o{p-C2E7)<8Uz~<ܯ=$ ^ ~ g
:L|4
W; 7{ygךh?sqcqY[_'J 3p~)ocĺrpo&ˀp')ӵ)X6LK\nĒ?POt}?_ڞ{{}Zu;T("4P䪣2Uh(Cq o!#wg];yj?e.eX(IB9yB5`RϬe?*n%Ǌ
jZN:mHܸe
,~R1Wןko+fIow>z$m+r<g?ßxAe9&%1Ƭ"[>gx6H|s	WPGGZ|:>	C(8#ƭPs֎2=K_^XE)v!]_$k<|1Ѽ}.<0lĲQ	V<0r22xƃOكK[PPWPEMnFC193 R9| <kQoGOnlt;[Z;DUCuV9U*2W{V$>&_.6O͏ma[RaԿjoYjmv#p <Ccg?ޱco᧏RјY*c|8$W~Ӟ	 ix>(X z6%Ueb*;mp&xoCxѭGcHcXnB>k7 	?,]C@:1Yccp`r=ԯI15ǋE /آ^N09S\`oFdxgO*IKG$]@Ca2pH# j|"esb?3eLǆ+xZ"MCL֚=ZL+@K`^@ H \j$.&ˉt
ATgr b?3Lß?<3?ZðM;fSNC(
wχڷ>&j.O|Rlfp>ʤcV:1+ ^JpTmnGϋ~.&KB&:-
#wi,.YG~9SiO?V>f.+\_K&"DһaT)<]*}m m ӂUҽ>m.pZ?{טҺ"bh4fn_&??jOڊq/Փ!:55 zGI
N' cLqBn4n0E֏7L<Ϩ
kK3PZݮaX-OgE*ϡτ \	,cb%Igg&`o\z
U+USNRݏp#x/PuxlZXŽ\FrBX =?% Ĩ|AS h׫~Οd7G>'nm|3m5VT+LنFrk_~_![lYWzeQ!
X21qUcEB--?i{{oGXE#\4#Uǋ|}cj-ޗwi[yIPRF˒	I5go(gsMxTswkM_:<tY`ݨ[,֍|ۓv}c~/b 	h2MsMh:ny1܂T 2	Ey5^)_~[[y?<a|W||55跖Ժ}iw2ɽ&jB@?1R&ǀ>#1P#\ӴhfHMi Z9_

u	zd/!#U
21^+c=}fh╣mԎjVL8_Z$JBR4GF|CwMAַ`ntXm.6n8e?(=EvF;馶edRL2\_$~^Gľִ}{QCef &g ٗ¿~no$
u^ͦ<6X@ GRDsI#'5Pړ>\t |[Lﯥ{̲"ȇyRyFFko;Gǖ7xL7>U	6G0nvrE}8 T>4|Dk|?M7^֤¾$;<]GNT>5\
 9mG @$	$Nz`b 	=Qng:\E$ث++<?)~1|1h>-_xHXcF& F||UV+_=[R13IH:N+rV:#RSjK0BHKiDт3__lC_w|5'?&Ʒ&k4-ՁeIQGW#ZLI_^|eh_
I's޼H$k7^u|!yagqB[8x>r=sM <W5;~7k|GL!4CHa͉C|clk)*}8?un%1Ĉ>]Ub_4MbMQ۬D?BS*k/Vq"k~o.\F~H|2ZlT wC81w?VaJ)J??hOH;Nu>aIo=Py֒V5ʣuo	a<7ߛ<g^32h]d r0{qߠ`g6o}C5}J6+QYZf :4Zޞ/GLj5omrh1(LgVAQõx
|+l|q<Kk<7x4-Fe%s\.~e4{zo0JۯJ0q4q|Clu=}k(V,Y[>k #q5KZK |?+ [KojRmqbsZu"+X5jb;8j"?e
t8?/č?=Ο{,wQ500f/ygHY	0{π/::oq[U n\KpڧWKES}ax{R_\oض\7 B>3:0x5v~xc=3hz*D5IdYyKxdeYmxV ]Lת YDKGZqZ75mswT*2|<uhKuagñK
<cB 4=1q *Bz4{G>\OO;ԙ67gvxK}/gtw
bɚM#2̡v(*pڬۍ`xPiK<zr7c}Rt܍ֿ;kٟw_'<:h>( #<&c<#9<WOߚ(2?I>1|;Q;f]j+61Zn.[C;|:n~WEo~VޛUOSe
VRI_zc'uC+xem;I3:
GlW?cόgxZXI}WHH:p$9;g
[t>Ѽ7Լ?~tBER4+5Uٖ(\/ˍ{WHe 
\5ÿ0jpdX',yt-4x/F.ͣYKTIgWdNEzGSEQ_,ISaCϥ}3{>? j~2kZl1[ᾙ-رHEє&dZ7%-Y#|rסkbM?Fd8ʏs38x^Ukx.n|k#<2pd̹>,Xƚ-8xTF8WM)<o<x[Wf>ݨh6Z9u27o?28s&<# I>'iv:ncoKcIUUǠ]O+vB<=?5Of9>,VX[#EDJ]
#
-P 	G8ߣdgp3]̟)ŻrkY g;{]NOxy<餰Smm9*@
v^	{MCG ΩgczR#]:JHuFXc$N3UNs֭YĻv[UR8#  lBGod84+sxߴ7?[]Z㇀wRϢ._]43ie%v_(oh ~@I0[IU	mum#õo.HRK3<~'|:{[yxZuMEp@Hfоi>,t4S-`[E;ôE NױW?k__=+].>ߣxf+OreF^Q9|/]  yoMoӴ[J?F?Z7PԗY 3?"	-Z+hW֚UTyO&8޼f
/ᨼo	&]YnDW:OSj<Q0_|zk4צk g]TcG9Qg+K/SR,Tsx!+6lʹ6I'X,EF_<<,5c=.S]ڥ(8 [uK/ʝluawڂwmgm隀R@ȠQkO |
HU^O4xfh`*OVW^JƩ%X´UNjJIMrЊH^,~xoLOD!tMW~pK
ЬB^v-< [$j|ͻ0WxbOh|qs%?tF~nҡ֬a׌43.V[+ڼ gr-
&Llyz#fQ29M.{\DI	tn=0{>3fSȬO7Qc>I<Mxgw"k}G5D[yz2xº<7j:İܬ3Ji1Vs+38_ \ԧ%{MHR.MG]R;תhn~ [fj"q5s ؾe)dvTU	f< 57|=smG<7w$}An|jY@<W~ kK| źx?μ';_:u](QwRI$Tcr#MJP~[E]6iwfv
) :q]cu|N =AWMѢCw+72P90QO,PBWnn33jsiiQ$pFUG'ӵm*kpΨԌin;~ P]Ǎ5ϲj/5./-"RY	#IZl1O	8-"X#@t*݉OUTX&ͻ%Tqn  ?x6Og^l 0R)] VtnUzFpSG¼e?Nl[%(7Hטs`m޷ƯŞ gcJmlm6iIN5T~o 
t-ZMķֿO5QNp-
l
9_SXӓ>W_?fխ4i/&PY~HW20(ֻxV?(V<+)4ķ/-^
>fei-r.x2]o׋_[8'VFf0Ӝ\烿d 
s$fH e䜇2PDԌj){AּmkXl>ߠxecU#-:d᳂q_oK5i\s 7GTwqu)~f*[	}+O[ 
	B^k7Ȍ/s?*#/ݏ2yc*lzga
ءfeb\)꧖-?!Zӎg2|$1ۡ<,I`0?=k
RoִfRyN}yUvI-&ڭj:YU[%/S/Bծ.ic^V.s|>Znզ֓mx?X!x/iv~dcMIn293r'4ќEQ _+ټYvzo ~x&5[_ z UӖ=A{Oco$pꢸL+W^ BZ<EOpƽG]?`u95,7R-'.|YT`u+<8-տzп-3Co2=+ʪ\񻌃dVܩܙ]I4yүk,L2796[o!Y$cS?1*>o2wM|w_־ڛ̐-f 㭇\HYɳ?vp
Q׭09/
GV_N1ZL\gTװ|3-ǃu"^90Zh7$TF885:rRV x/4;RxZGv G8A߇z5Ynٖ=FἹ$ctl?8?h{VI	ZI+7e9l1Bcld!+(ݚJQ潏uڳσn4x$fkkEZΪIf]ӱ8{uC.&<?jsIwf s2yz׊}ly8-SKx$S(t,S:k^*u($i(O9!#@۷8N+9uo,hiU<9 . y^])y;OuZ6v/ַ̿Q̥_[Wikfk;@2@U kcPo#تG,1ɭ
}W ?M2j]Rr+v7(AT>7~П<k6'ԣU[,DuZ"yhW9=nnTs>3 Z}/|;v@?%Oz~jk <_D4+@nqr[{O"='<
 jc6~ӡZHc^;U
=:Jsg!o2E @{;hrr _^1 lݚé|=ʪJy,ʑY~ `|'ֳ>쭾nO 1 gpTQ:w/:$c$x_	x;IkxT$qā5 ::((((((((((((((((((((((((((((((((((((((((((((((((80[OؾeU
6x_ῄz>&kb+#_O)$/*H
	a_HWז:]Cg4$<4g?y:nGT.OR.=0Y4C e!6r0?{8x84;÷>
6m,&Hʍydb0XN@< گ
xN%׋-d/&w[Q2Ҩ	*Ep|`gIQj[hT) T>,R2Tǖt>\累0u|yH$nIlav^%F# ZWH;o`bpJ< 5aO>VoMn]1C 2c)89o 뚋xK㗆ꬳ.ŧBVr6gZd掫㧚Ryº98m弒(#uH?FҚ KS߄}vMfKln,v9$-Ӄgkk
:෿<ېRW)QKjK!@|{w_kJ7ۧ
(gּҔ/sJ3}BZxwz|'5;-@M$b':F<,Νc$AmS ökfgB'?ZUgch^uқH=FVIfCPD؄崈[,Ӿ|/>S> f)\¼F#YY+R+D}gzׁOoy%օRD.E\/2};bopMм%qi&eA9SCmʓvsx׈ټlyeP:DU!OĚ~h#Օtl/ v2ĂH>aM8+GƘ'xkž𼗺r[D.
I dF:ѿ&~%y{n\PicS"Oi8lAұ| hvMǈ4?ZY[ZMW\yj:c<
S |5,>2<@6xI؏ެv u(7֔e$t T|E_u+-b=:+>A/"4CLpO8ɯhxMR-nbn!	Nۧsڼ"gۯZ5|X-iڏQSD:ZOrw	X\<2"ڜɓpu*KN<cG'mc̈`7lqۊou5%Fbd"ePA$
pP=+fڋu~qh|T|M&;[G& 6F,">4k4q跟$R/EVPxG#
q#%u<֋W=>_짶='#gCW?>=Xf~zm/(p^Xkj<򲷘$qrT.sVt-zHaQc$|6,WBALȫmo>04\>a׻Ʋ<O aGE ˣWVk͸}&rAy,l;to۝?\hvsꥏJW˿Q륇:ڻccVz2z%}Kz9-?+w@Gq'? m
_pԤetsVcLM'JS#!mY 939(NU
fHo&ѭl  [qV~cf摜ڒ.xSj[ޫ̶2?Lɒ>7Ve퍣B潏xQtzKƼ6 /gǩivDeKSSz??>'_,J%@ gPLh;p]<W/\xƟ
Muup1]H#ęoZ	SػvFۮug瞌dO:Ai;S#M$QXL_7JS]o,m4cKKK+[$*Kp폔
7²x\[mN=B2Y݊@9a_Ě3a.\PL n#cdA|5w f}w$TSit#+*j>n ~ڿ7m.PE'Ε4Pf"$V\d3_S~/4|>{5 ii2/q+DdPSОpHۺ xvx^X!?zo >;_̗W6BDdF_&۰8\qyDЋ0|5 c^&i-mV8&"K?1
]?'trxN>2K.ê,u$̒.
1Wq:CğQ
!<y[vHͫKdO!6݃iM=OnV_?<nPG5Ұt.e%^I7{w<c {|` hMPqѡ;9584yfVS3*!~R9=k?;a'ѲXxQid=S	X8~_d״>1P}Mmg%q2L\wt co}[Zs*XҬ<K;V5uMKDr}jnmj˞7_GCfi#.NHp۹
H.Hb<__S}ou%垹iii,3yTI `	'h$U_
'5ٮE%tO1p&1F O5%?g_|Bjk:u
[WT_3h W3	=o:RQv/Ml-cMyX4!@'$I7_bt?YIP[}J~3az0`A+\ƽ4:K,x|<O*%1Z[.$+%ğ/z>65 xͭK2tNR7oQGT~$d^@8<4,k"H484Gğ匒AǨߡQ@ܲsl#_xa<&wd#>9kU
O^G2?
x>S9&Y<P0BJqZki=ՌO$gf8y+fX"ϷQ ]45Ծ̞eI<0ҥR,qؑOa_2Y]V1:[J;yakdH٭WseFORIGk"a?7FqA`7<C55BFwcn*1#Js-1I3H74qpR[Y$ }:v1+jfMnYŻ[,[?0]vk蔵[@mDOF>)_Iq Dl[[/Okpu|kˮdW|GʽzώOxk)v|Eiqo,Ͳ8o!	? -c~MSem^/9ahnbeX]<#ԇW#|{	;{cהupAk$*>;g{}>m_E'c s]Xſ
Coh_l.Kgmq|w?zW;O~=/dQjnc 
g{c</a~ҟ_Hi>]k-%o!;"[ʤ{W.+Bti^.m֮̚|'F-7`8<3ׇжQI;7xWKzt~
 e~,Xj('^M;..|;ˡ6YԔYXFGA^o 'sZPOŏxi\jdZ4Heυ}LF@^ce	sɧk*̭b_Үdl\KF' c_a[7dԾZ ̰\5tlϾha HJC)o¿6YƄ-m4uxͅ}lg&0s<>I_:*PMr{/3W$7>Qs/$PxkViӮLH[{jj WzQ^#
4%dmKTGծ㘆	lҸߴW7iSGuXnft]ro$B۪[z
yOD֑Q{7oٳ
auO;=7ZVY-h͜(cK'y8_ۏuzKN>%efH 9ݷ2zWxu[MSThΌ$[<Bcל/x_^1==bTr.o ~1o_f9}vmYZX6K6]KXPSl c&dܫ5_Q/ծ?ďͬ9eWU2Nѓ^.t
|[-#ڵ3FcᙵQ^cYgh>θ}a
H(o̊qTRZu/W~W<3ÿW%  
&ŁдHPs'䅹R0Hl fO'?
xL.ժLсB,@ʨ8q}x}W֝g'n$SCڤ_Zo 퍷MLpwȧuGycOi#<?/xw76m:ĩ沢2<sJ>ϵzg4-?lO
Iy% <| ]7玴]Ĩ$6,6  kYm ԭY'y#L,G8;5:sjW䔯&;'|k8[{X$u}{[Ofo iVOZkL EGEG#
ׅ</k
[ 妋 6G䓞 wڎR$w5F}d[[o#޺Z>ۿEsCnm5m'Qdj	{5kNPޭc֡}WH DF=1^+E|nN!|yt
w},$eI+7ߵgv;{5~uIDJgb0J%O
ԿOexm.YEQåŲ13dq5?<Iշ~Є6)ubIet 6#1fg'Yx幔Qv= 4M🌴Z+孮Tc%BD2xur7y?>*'^ZnE<#C-GkaIG'gGiiz[[]|yo%ǧ30q UcHb["oąI2ҁ	u==+UuƎzg~?5e)1KKy+?֟
hhv1Qh"|~WπY{~XnH^4
3c 
k]SIҴ{?>0F	QryVৈ''7ȿ
Hg8e~F7"m;ڳ`y+zO?~?13i".5qߋ p?^$9^̳;[daDx>xgZQk'ºLq\QC_!-+2g
zWW~k~"-CCQi0Iav(vVs_nxjrNf;f*DqkK\Қ~4]PS mFKk/Qdydb= |?྇^=CjF8akb G a#oß:-eeQlm6bzg"[ᆑ'z-/ymKp(Ҝ޽[zZkC~~:RtS&R۳\I.39$9 `K$xtxZ4X{>svWR
*i琹 [${Wxͧ5o<xg
88䁌 Nkt٧ƾ'GD:.rEu-ϖ3wګٮ==uP,w$r[,st*?Lw;l\y~tO"5ęiYƜH8=OzF>N=?Z3to#X<ӟW	].T)?>~7~(?h2\oOXKhJ EߑЯn֙?P/dQaӭekDJFA8=0kĿe/M&yH5C%<bO-3ۜ;?>WIӴIҤ3G*x߅&-Z.,wbAܷ	V1GϽO7..,8ԮLHˢhPi6ry~f_oHyH@+ d|w0{Puw3yli^@~mݏ0H<WZ~x^]ngpm֮TʀfGP~ֿh/zZW|]L@U?OrǶMuGIˡ,-w|H?ρP-ğx{reBn$ǢI_+ HLmkdqvVVWi_Ş궿غp.rjWV#&ON1[zݬ_'r̳Σ՘ؑ1	wRl|Qn|Jׯmt
-.˟<ˬƧ!\WKKK\.'e{떑cBvy@ o
oAImnplAX`ڦM hM`7*wz/Q["m_H !^][w[e |:m:+ӵ: 6˿2C:3K0Z+_g;>9 q
_z)͟*zVA^WA߆#Io3\"ٴ:x'޺_{:~qE&X๒5*)[Y/Y#nŨmR?wms+Evmݮj1i69;#p̄򧌟Zc-av'bq ]1ޞ[k˻(sm&($mCu5PF{s+k>-xCƗ|~ؓhvk䝔n qtkoWԤ0|̎>f;c 9 h
GҦnnǞxZ(3c#vw8^kd;kWY%P\O&~l5/R<&yCM%$X݈{Zo\GOfi0Vw4_5,Q۬q*- 1<&!xŚ\^xĳ]IT']l.]FpTr(QYykte"@xo}?TGv<7DzC_-5^xSյj7Ot$'׵{gƏVz//ݧ]u ?*RQt5- 7/8𖟪zWHobXY1^9'NCAk{c]7JյuM=\OscF]5[
ݽ弛dHF"ڑ'cЇ4}Iip|;)n׉_M-I~xAG<'WͥVD7	+`/ +uόTZlGi}<M"l
T8
ʞݺ	g>)]'kbۼ0c_ Zo4rTo/ٍqpr;dbJ~iriZG'$eE:ҜvL57N7h6
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
ϊW:wS Qc9F=Au☃\~qSԍTqh >,,O2wm)x>#2<`&pyGA;>f-CU;3-m0lqʪ5dv7v&Y5-ٕngC5c*&̍$mX]Ċt$xIc< _3*4$lcG^2 ?bF]2PIHe<*y0(3zdֳ 	E$ ?!RcPҲevezhxC<#gq"AW--֥ (غkaL(8u<O~ƛms,v'٧pE%B\m+Oijԧ0iQ<?Tuٶ-׋沸E^8G]qk^k
xr]BLhamGJeh	lO\tax24Դy!aMf=AF:ב~ҿfuֱ-&C;/p';X9Ox֥-mNTɿuG·VVk  fY7Aw\C3c5Y$efUbe`IW?dZvţOĺO&Q+<`_0B+xX6rx+Ykd8X
g#8ymYU2^(a5c:Vkh 㸐OOrI_|d4:񵼒"|͏T do)eAuGy^vlMs xIH qxF'a`|^^B?孫훌  WYc--q/yC]s=q$: ;%A+IՒ,b;;7>Lh?[ݒ?;W#|9qkxosqA5m
	 5,oG/$MST|E/6F^FaNX|+SԳW>w a  ak}?j^<f!cM	%K o}<qFk׺B[x<P|p,
#$2T*I0y+M	Ɓ=:.c˫QH
@ezs_gL_
p0iex5O ϵyu+N5!;9Mmo;@ѩi*Qc,`WrWr\]XvC
IY
5#݃ <'OAյ|%F{[YK,0$&R
q\sŗZ>*kqJ;|]hno8t=YTtSG-:._MǏ5at[OY^C<,ȱ1h\Vo=_	~j=jh774d/!h؆d t :856;<e xv|;yio??|C
ki'T{mCNkLen?	2R:UJK=5>"|V<x,}BET
$fFuH'Q_
cRƭoi~Y[M
 2+ٿfO^ iu[)׃7ˡʞ%Ia ol<}r3Mо:Ŗ~]MM*;7;%[ x~T&)߽1	ԅOͿ7?^tmwÿliD<-ށ]JY|(q M}ZG:N_$v{-Zu4%LA{I(=m7c
*~*EMAoKy5ywm@ `d@ X//-g*Mm$?uf3iz昵:w1\sm(xc>x5doI#S% W/'pe6א߲"|^&[ {#Qu"!W -_[O|}xwVZnXMi4rL\|g`6Ts=Ydrj ǴEY/TCԟS[~Ş&inT~.\hH~|Jy>1ц.ጛD˵Z.~_]u
O^<fź|`̉| ,G X-c곎*Ҵ2Gt5B79|MxHfmR`R6̥2$dzVfܬ}L>H2/kFNW5\%3h"Z¯\-cY6o  i5cFׅ|1T]B>Xf#Bz)
W]Ś$YiKg`W-R{sǫ['#YWt
\`"%[|fguTp	y8oc2p|l/e#r?rO}uzFYGW Ky/r_-tFMs3k~*j[ [q?t3_?|Y̐\.qս=L|'W?*=> <>|_jEk{h>ԐĮ'z|yVU=x|>VuY4R<
&ߒ?0@y^-PtTǩYy_2H'*+ݕ4o#KN8]'ជc趱rf8W. D׆vm|ds}[ɓy]y1'2;׭0៊7?\U!
g.	R27
yU̿	;q}jq_èEo%XJY\Qߚ\L-WNs'MIk}7x_ }[y-^R:R #y յW
ZE#ф?aXWѿ jb𽵟,%-ti)m#\M4sƠ``
'NeolV!I3Nq6ֽj5)8lx՝E'&ϝW	DwɥCq#t3/ EaN:G3ZHA4*I *~Xkzn[ZⷝLs
Z]&֎4ٟ9:I/DF_Əʟcy_]i3Y-rZf1(;?E\Eozg,qR}I==6.>\k
Nc|:u^;Sͪu?.jc1\gc!'8+1xYI?ΞV1wԞdoj}ϕ=Mx[^tm>bK(ą@}	@c+1e7>dL6<ذ'yg0u\\jPGg4r;IR q򘌖/,ZόښvˠLa$*8 z5+=QUf[u"u]A߃_Fk?O9aWG6s1ql~T!F<ԏ<.\M.
g9W`ϿoFTqhGS?n\ԭt=[/5
QZ_@h7>03z
m5iH@`LPS|ųinY-tmMR G"Xu$˭JO-3cwr[+8uNI{Dz}2ġg'6	<bg
mucDfo-5uTam"2O]?k ࠎy +*qG&)MOu1׉B+':ּoY+Ϝ&<Kv ȫV>x=  {k}cW@fF"#c;X:~xƺv4Q
Ď)6H' e{k[SJ1|M7~%Y3=MF[$ S\z
~$_
s.lGU 
մ}.-/9 d]ĭf;_+{XVke(6գ>Qŗ#J*6RMKQEؓ^%׵ӿ]/ǮxCh㸶e ?z>k?juWˆcː1o흺Wk u]X 7- 2e~vGfK+vKm#xxYLxfH h _N5#$WG /tjM03In踐ߦ	$ $~Dcߴ4wK[i$dd96=Z2
$kAb勵S dmJE^jdu:T ]@vWUqZj4G|86׵Lmjng
q^տ  fI[xVcC#̊XmFe|N8=ЖkޛK՜ ZPM^G-nR<|,P4lx-wFfݰ+
	JlQ.fTPQ"z?h _mu/%&%"1O]jϖV2qex-4$mޒ0<v++twVy-ٮl"g/ :auyK^6q:%}4Afeڻ b;ڿ%Fᆛ.DcÚdr_?;pnnVF<dmdەɭl{/^8+]iu[QfM/O_S$4
Fr9{㯅_5+ |r𝮱ŧx۠7e
8ɔ_4g?:}R<Z5p5TL@kZh;E دfɵ]>G
'n5<Tk?Ga?($~Ch8َ2c9902 Oɦ~vG5FD](xܼ_մ;+g_:}o&mQxyk6@B^ $dh6xoz.Y\	c}=yja%x#:8Svz5  i]5uct_ΆXM8b癎A` վiw
ROh*^Ke!#nvV9	'=yo4X^(1FZn8$\1#H>u+nSLt[ȭeU#U4Lß?/m	[dcll Wv7k^
֋qD4Hsr|qlWB,<[<4TD[8̾ǥz7ςxWJ[]680QfY3Pg545fkWFG-]_\jldPF`'BH^K_i*N9'h,?{ЖɫkWZN5ܱZіR/׏ƼgPٗŭ{Ok14WՙB[|yk8:T $5g"gx[tEW7ږ$#dqQWqX{?~ YZE[qןҼ??5>1M	t]28du/ߪK1\Ok ~??/;RG2kip~,nRZq[?h;E6=zGz'UxOMU7XҰ-PMxN J<7htɫ|A$q>إ}[]k> j^"%W2\X's?{wX>.,8:+9fU-,
8RW tm;#þ̚PMR(LlV)~qJZKYO.U0m=ӗX6E:5oeƞm5L (~ׄ|',j@ Ok~iNrnԜcxEl}= 𕯄<{;[HZN!X&ּOfn>%]P/'bm^9\LUHxyybt}3$xZX%tV3}w_ZΥ?徛GXMH=M^Ah;s޺/),? V
b|i߇nɩ]v8U%H<X{;տn
n<;agomS+3K8a9*0	|[.fR;J+"kvqd5naEkVpa"
u2$U㨮UUɵkJ0I9=Ϳ @~:_~?:t̗%2;6AI^s3^Y:
+>.?xPE	*7r_MIi=ˢ<\J 'z 'iwVRah'+G?_fK[g8
E`LvSHzg<+D,5Go:By'sqk{_iQ}~o9`+_x|a
&fo4f$lY/	eBaQ7ֿj,|_Eh1t6	gu;$@OkeNv3e{A7wګ@'Lu܁_˅T~ bv5-Ɂ}ƞ?R|3;ip3(f8fyI$<c
įbtR3o.pN>^}NW6ꋒ=5*S4ǈ帷ޭYf!mCJ~!1w*!N	R˕88 k𗌓vkO
_R})/n-L\&^p:[W٦Yj:N1KY,:utg1a'.Ylx':"Y6%q" >+ؾh/R._[O@aCX
++ߔ|1trAj˒`)-яWT_kPq WxGIibr%$ Ӱ]TeiUw|O]K1 zW+fIm_G4IB=񷼶CT(ܰcE;GSzo㉜6> 8xDOI#  ;mϮڹ & K_ji:QT`&Ӂ&޽m%ӷ3B --jxTм/]jZs_5QlW$#HR/dQ|co|Xokl˩#Gqa*P-9k?|-Z*|z
k"\M,덅Eq~6VE JҚ	ֿK-մEY,Kb񦢷1Z|XܢƷ J,9l>3qصŭuL#*k5&&in%GHgv'I'&qo>#t+
;uxXǘ_:"YStO	$Ӌ>iTfY"uZX[H֗>(|/0JxcqCiwjon$`z}7 ď|]RB
^^4!1mخ+@fD	@Ado҇y3?Uxbh\с\#0ŁWk?Sbe}x^ѸX1cGom>5;3gŒ-eIyfVseb~/֧-ӊXzxZ5yc~ W~#$s pO	 #׼~7kI ajiv9ny+ׇ?{?o_{
xx~zk h8wuǧ 5u.?ž
k[U VTI	8^my᫭4L@<gs!''5 Cߵ
gX𭞐NE
$WǾkտg&+Z=cOfIQAH8\#c޼ueʷ=\7%f| Şb7S~k{_ =
k=>1["m=V8w,0c7\|24;+hmmmm`
(ª 0yͫ3P,6UD1 {\bvy@(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
v|ɷl4`2Xg=
oW/Y_mُ YVv'iE^iy5M{Nc,cդBNRKF ̭+۾cۂ>nkKvl[:P+K"#k`$a^?:"!V[}yt;Ae{s%uinf4Fo-F##_#F.TOTy}KBa&ٴ<no4	lz:3\&[pou
 C"#u#Gjq4K}FXHtJ|S)-%T 0 >uJGڕbəA HpG͂+xԊ3FI5k࿊*?kO{i6z	ݑ[x/o庂N>/ޓ~>,XiԒ G\3Z@ŖY$+q$7[xMEKZB@4vOdF|X~~K^Fya9ɀ_g\dJYGgL+v
~v:Z;IQ;	l]Tu(p~zW?,ZKvXI	8 $	ȯ>ܚ}쌁bSO 9J A?A_:[	}a)E=~`kYb!`Mi7𖍤hr]ka<\{eb@
O2OJžIP[k}!#P7ڤMjޡgnn納\ƪXlmR</7"+9DTkTWO8,/<'xKTSʥe9@'<cWo>1Xlma`kX;A1(e۵	k/H oM[:͊eUX])p9_ֵSJ۱)su> k|#dkcaq7v'iPny G<g^ԾTvpxG *B$F<$%W>hKnWGF?M%㸝Z`<F;Ks{?G׈- !ֵE.4Ӫ]Rt%,2	94x~oUgs58./g<2B꤁55ac 7`{|/f|a& cG!_O	"@89{7QOYt|QaNKyij>U
*OB]զSiof!-[e%Fy~XWs?ࣿ<[c>!կTc0:e1E#߽z~՟u7\xᾭs̗<ךyphĒA\
.ZӒCC?e|8OĄ4>*ϫ6i,|'##4 xv?^eu
+Q	fHOtkE~xoU>2SIO<?mX&M?QPVHe`?>ބ fxM6mشe`e׽uJ3QUs
 A~/|-gKxn	bQb,QTFƣ'Yq+oϊg/>3|Q[4w]m;.cbF}_*Y?χ^,Ms{^T30Imvk=kLmV! zz~~*HԢ;[}O~$|%yῇ>6uPz$Zj,];wnpHo GDx6,tK-[E&"
1#6CkOwQtLA*GBr}~ |5=/OCaӵILw0+w#;2`bMy}74:*fH4RXk%RM;T
>e'ԓ+m<[1\YxHGHđM'nln85࿶)}e|7<+2d'՞2m˄x\`hwzMֱrUMqh/Sqjoc) 0<]Rz #.gʛZ[~&3?6tcOu+ǃ᥏ö) 
|
Z ~EE͏6Oqf.H'WIwM56\A-x:ռE - úIiō$8*,h Y8k᷈4߄^t8K6.LM*Tv1%i._ DGumXǥ𾬗--Y],r6$H$#p=zno1G:p4~%I7
0C{f<J
B'm% wv%.
Z]}2ɤ)+aq";?J饌w1V>IlWPx휋sX7Q_~wFOimCe&pHmxoE>˹졖3AS \q>2Vm^7.6%]beYؙa}y>s\[0<WfW|ƺnc\bTrO+<xtEv,B<uwh~7kZNCԯ!U,ZcUH3I% , ׳G{ǝ:}նcbb$=:e'n5DӗOk:N|ȕN{S~o%ݬw7 Hm>Z $0F 5]/|ܷ?vVN:_8єyeō.#[D'XX߷ߴƵkv}yy4vVU8X`#'sHI$ʿE1
[wˌ~Gq>#5|x Zg^&-6`iLLg_,# gpck3ʧ2o,c# W_F|`4+M:\QSLN*?
M_|~ iik{/
.k4]f./%B.Q	7 <\QֶPAmm4?kH̆@9vr~+&I{yf:>67jz	81_*4T֍֮-V>׾8D-|⫏[ڮ-Δ4ۧ(YK$C2+>8&zƉes%ݩTUwG&0	ͼީx>!q'okk/u}2+u؞*<2Ik
gE[vuX~[8aZM} 3o^xtr=Λ1_)ˡ>ۖ;OcIq໦D^ h`&]zr̵EM5_o&ֽ8kI\a{_U߉2j^մiȹ//~[;٤BP5_:K[#P`pO&6־	 ]AixK,IR2 G.HuЫI[Jތݽ3c.< *H?ҷ.	2Hkx->;sF[D~ǺnnH8c@=H>	 TgN8>Pjr %ۓbGOZᩓPsnv<GT[y<GFŎ1Ԟحb_1w(>O+ާ5[[Yp$ɃwQ1hZziYOqEs:դiN_9o6<Mf ]bQ J(t_i9^դ2:Cy-fe\8s=0 OO
oO3Gl= QkC6|G[2Wxݙej!I|铊|mϓ jJh1U? N|mtcoI~~ 
	&n/!!Vo00
HP2j?^ռk/l!>\)r)hmBJ0:O;?CGE`_U~x2']Úe*J?P~5_Oc}wmgtu;+YƃERyB1"ᖒ	*)spcI <jSWaSFx ٣@BdH\Ina}A>8|?eďӵk(|Su4Peg$WstO	]8onz`8?{,[GIk=C*MqmV}tE/4gx5
KMԴ<ACq
G)6pRE@(Bg0xK8xHemYQo	d_w<{ճcZ8cb20>eޤr8>⽌-+])h׼aլR7u夸bfAcy𧇵tu$r$*Iqk*@n5/0z>UŤ Cמx/צB
5;Jm3jQVy'E;ߍI傶ڎ	0i`mL^{`_uG߈ڵLh~dYl;Wq>}+M3&\y3dfBn<{Vҡ)R\Z*o
_k
 0{lWuz/x[ZҴm3#;<ulHr#kZ'&Vҭ+cfio<I}$2dzTO[Zjp_m3djǦX jJ6Rڞ0F`?M hz^x/u𕬷d{' Iq
%yW
6㛫%%䑿dq#1򑝣좾)/\	4 k[dUa8,O5xj8?'ȯ~뚿|Oj~Vj^_M`_vRTF2G|[ewi5 |m NoogocKnPĦG0d6'?e;wYi 5J\¶<WޕjZo?:&Oi;Wjb[2G2+S o*ZJ^'?T#,>С3w>u˸z|*xJ=[⧌# ok=n_ҽ/HUsdNaTڊZ[W}A⯄(+I犼EZ;`ך-!YѲU@¿	b4Mǐ̺F<_vv2,kFfc `I>}-_
-C01 HkOc?d-*=3=U_L1o)F$_1Xir:w}+JrZTg֭^7 fKL{{=fZl4w*O٢!.瘶xm-n/ٻM/eלF{oMs434sZ'f$v[9LnnގL6gH9Rv Oٴ&Vv=
ɠ@7 @qa1A^g mۚC_f~ιXCݤy46YQ;N
k@4zӵ%š[d@u\3De$, _3W3h/8|L¶+?m>xR+x|"$(UE$
Đ=@ f';⇉Pot`ibeYFzWS߈|6_||,~5}J4EJuK)}=}sşEҬlʈl!pNn+_|AS7(xn[*x񜖜{ϗ	>/~T5L, #PYKí:Ş.[?1	bO1fϠ5jGW[v-~ܺOw-ռg}6vSl+-7,a~ҵf7{T?/+1}7VIL)B̌Ď
5h=PQ
I'=feL65{Yry8H*VҶ4K7h7L򛙢$)'޼VզӼ{.i$[klmra@UQ>ꎭݍ})MwO>!ٹ4RIho&_<&aHOF99,վIOxQ8[_"l<D_=r ԞUv|Uk&Y[r+GIBKEH^H+#`s[	[NգLvdRvC&^? 
ᇋdѭ']܋o6~e7E'Tp%)¤\b{ (-A,k9. |Ezǆi@tA{YQ"w_½BU$	Gڏ>_<k*^D1*3|O\nK1G }nq c;),0Z}屴*}jnw hđɫY[XYh 4 w-sW[ݹ}ïFW$T;U+ l|kh~֦_Xa2FRDWr"7m+<nR&ܪ<k7/6կ8=\ժJ6taF\k]OJ[{/\3&N+=BTExRռCHUSs~}}+Goۧrq^|*^餆x5[YU `yfbڊ>1OMX&-u'?kgbΕt}տQZ\D'Uyuݿå\ j+m3كJݬس9z[wvwז?iFEkTWqJw컧)ŗ܋nwxiw)YZr4o;Hb9e?YwJg\ rOw+ntXnrbQRĀsןzL[]55'[f[n\ xȣmNoź\	8Aw95hUAq>jiLi82؝_ƛw6K26ӻr8qziǽxk'E474vwq&/Mg.y"W𦙨/nP7`ps^}[,|/\O]"8`V#a[xv\7u{enD^k$>8̖0\K![ብN9h¹|q^{O_[	o#YWyn#6vE=+~&VN,m&].F}9#ഛ(-a+LJ:FZJ??k+.xl[\opJʲK_gNr>9'ex{ĳz&sla
1#@`u^/fBҙ
N|jiO>gcGNqnK/xMہ#89<.~sKk)$*ƿ6b1Gx~_H\kWN>q0z
bW=-uW7"(ҤMP^[)mpQE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE V/Mto
]]IG~>	1ɳᾫ \*e~ecQ isɳx[D+ow0T|bkM_IN-RYaUTPCus$Bu18qkվZA{jW-$s\| iԪٞLt8~<)EX]yq豢=&eUo	 -pk翄ku+K:%iɞ; qM"mWkΩ .$O,.?*
+;כʪ7٥)ѳ|<i )Xpz:W% #^ltxoYgx5;	h#0Tl`r3޽T+hl?C߆[A^"WXm`
F+ƿ7RxOᮈֳ^M4 ad9kA~a;Ntt9F[GCZOO5c-ŽƛC{"DTdh*TP<Gǟx\c<#mgTlud(du6۵ |O%ռK·ͬMw=؁U\8?j-=u C#ƭw@xbJ3Qѧy#(=,$CCH^62 Z6_H|[~lX?? ʾkUn>?y3ͼt־`dm]rjsSlTo-sI"Ɂb<ǁQҲebѕCPӶm
`|I35	 7,wG 	:Xw	{ic4%o6q׿k	`|2YYⱱ GO3	?VZm[::L@PmmHL܌wW _=MK· 䵔q%MKf<)ƌrz׌[E[Sz0cŋkgm&RI,`ķRMx1ȕz\ѣ3gcX.ú]N&YYH ;J2g^)S찐dT7N8Ǘq~?ܞd^
fiH$$쇒O$zJz|
䣩|v|U=x{MT#Zdakg7,_hKWޱRxp K62_Ƽ"C \5ol2=j2q	4ퟲ߲_ZoK{vTGLhw_k51ȯ<	ҾaVͦi6'9-剅nT,Ң7J7<z~~Y4^7˾kY$Ì[ J5Z}߉<+ISOռ'0ЮTPPWFW!Cg5EQmZR*M 8/ g.+S,jdp#_*3>wiզgCinMm7 Znk.tXy#wVt$dmG샕9Ν?4íM-[VMu$xBog&%\W$S~\1ܑq<C
Fߴƈc}&?jGws-]
vM^=t~Ǟ0ŏxoiVinHv!_aQ'<`fE0uk}
%џG\aQ!`zuQZNaA6'Oi>KY jLwB4{<(; WߴO6%>/]T \|#yM}e 8ӴMkUL23ʿ<ws4[g]@f
z8	FѨr#)(:k= Bt??Z>h=>=Z+Kq
F]H'^OMK,uѵit]Om4h#3~H!x=/Í[|%YTn1R}\q5S+Zo47ZDselpF}+ިqٞχ+{㯂v t8uYx|Զx܉ǘzׂsо7 M	t?~ ^$t7z
H!y#y]@6%_"<q a& ٨5ܣ-C fo˷99VExTme`]E>osgnՇ$;Ծ hVZ~cqk
n6
..Qwѩ,'$tO2I?|[fE)m$:#,M|`~U$}m[i	
/Þ09\JULP@OWi/i|aR
2QPW#߆O)=
YJfW1<}JqpbyGx
]./?X[7vKc
Gk#אG,i`ZEL93^?߷ip)*i:ݽhA!h   ZZ;)edĶ /dglخO? o>
D<ĭ52Wc#>5::;=?Ov$vQ?܏k>2*M^}9#Y	g +c699yw?hZouYV൝u[#drq6ur⿳1:YWqJ䯅׷[Tb)_ٻ-7ĞSEz-bcgQtD8-kGG1Wfmou%Kqs_b_|֍]kMxd^jKKn~BT:Bdc ^X^X5絕et"2:8)t{'&"Ϳ>_^"/,?^
.mH:qzٷxoi  {aEfzo{mUi_h<tg˭I՜?je]0{>WOd>ffOnPrE=sq{ wOx-a0F T#p8lg~#Ю9-nI4Ya7q±?`VGL3^F=H޼g?Z)Fq7VTej%?|Y-SKքKwH$G}
- X?hKÞI<muh~tp.v۹@|IϚ1ٵYx`dY#m<ǭzAg)okCe`{ǇJ*r}u=*y}*"o	}=Ŀ7*Xʺ}X dlsw:T>iȱ;$@BuO=J{)gI?v698
H'zi<esZƥ#¯OrG?~!zHKM"G;"0y	h|Rޅ$.vCVJyJj^1n/[@|
z{x=ծ$̶휅$U[U\Ҏڜ<>.&(5k>	đ_O;?
k_ N#ȿ`ٞ#[R*]Y?hoCR&Ge%t).|0 x](][ф4Z|~W|3֭o߈uk=Vm&I+qpp?ѫmn⽣^ijE߳p?3x^LTE3ϣnm3O
~ɠ2\XޛrFhxv
Vhn@ĄsW>3=ռawVwex.926B+W\_Z]V;T簗je1:@ b?ǁ8h~!'*_Ľk^璳ja1N)_	}6PԮ43T,$kq(6XC|GD'Q׉-?m~iŎ<H9b3zgl[n5wº>RhEuk7z[G(y¿jd~%~/hUɵ=@R[zc0+a1r>(|/cjj*6q.j4aڝ⟆?
g|7;2=6%*ێ{W>>|t' NMkKfϬ0yhzwْ)&on21 ^IGz:+ާNfVzy Z"˓4m>B{P 2וj_S߉>/#8f%.S(H%hK%״q66B3w}g-_y!!7|ߓxnWMK\2^sh1{GJ똦^~/Ps?3N<KMڴ7Ռ+6#ncK8| _* MyU_&nxU5m-99݅*;пd~!i1S\]͵IJθ9;W]!_z+Q>QFvQGiz,vG5ƃh
	[Pp;  Ǻl3*~1Wμ{LmtPn  %~	ncڥ|˻?^k:/b>c|'ĿSw&¼"+2U~'MG^nWu/u;_}s$M:q;~.c#1;U@Hc[?0 e>+-!hz߆3^"<93 l<&@s?zc	.qc
rj_\jOl?{*ĳ?Y^k|qlTk8

7? Q̥On]sxg}Z5Ryx_/cckkgjg"	HWrIMz>!i^q$[|#F>ToZ=oW^7׋&;-d[mtL̕`PӚ웨 eEݓ
¯~9;[}k$.ik$"1}F
n  oK.3,Jx7N\y>^W #5BO_ij>Rr,H	\_

{ROIZKo1&PU:,XF`~zHåfI"nV*A_l94j<9|csj |в[,@d Y̰Rx#u|k+KbıU
o25;N=ZkeNَ
/	 <|D-׼Aux'E`f)duTM9 }	G[?U0G;Fsۢw_ ^-$8#. _~Ӿ
x!I1oh`%A< fuHn,od"1Β(?
8YѩKIQ;}GScj oKSOk1yO̩->w
x_S*伍lu[O#sp,B x?,9>iٚ?yOoe;W#q^*?g 'd־"/#p=Aq+tJqN
m3J)y/oϭi:¿xT|_jgpRLi{b-lBF(bO"[rF(1Cu=z FzG鮅ї=:G6
yG'ؿsxö%}+\`fQ}&$e2Si#b[YW:M#׼O?|M<Y+dEGSR'zZH Ɍs\ noZ[\ῇ
u?ʷ򮣷m-d>pqgzo얥#KCmRB $sjtXt
Zh[ɒ	c»JUjs|>rM_Ǌ>1]R|B	ͤ;AfѥIŴdD
;c8&OѭO6G~MmE2m']ug*`ɖ-nP zn+,-ŽŬmm煡qc`rQX՛;hCѼ!S@9khG_kR<p5ׄ>ƪo\g '<~ǅٶKo5<,I7	dw³᷀.fp"rK` GZXanRt%S(
>+i/tR
.k8Xn u?ûſ/_ Z[`XuWnnmAH?4.&ehJ͙W_떴[QhR1Ӭ)oi z|:yl$6J>X^   ~˲\}"<imۦѹ,y4c$eŋkH^yð$TG'cũ]\?Y>j
T<h9c5hz7rG2La˰mLnt֞:bV[V˘Wn}UO
Gm{ˎ8U(P?y6Vlsz̟žfW/?m~ېnt)	߲J9[??aNgz>(t?;GaWkѓ1ncGo$׭x|
bL	d#cy5+%Q׉jSoqʪ6X[B0~[9:NC};|ޟ֙'rx Σ 5cd7MeU]p:«]u^l;σ5PgqjWگoviWp& p9Jo4r[\:lt̑0# J'~>mDجečA z5I?x3A|Cx>OVb]rTocǘ/,1ʌkVW5im+Sl,R#Vˡ8#] |x\M<Z9oL0+_XۦPۤ뵔0W;Lѿg;[o<m2+DLQl9@s<?.n#I3	c@+_"%֩CuqyA<#o[[[kxV2~ƽH^+G_=5,RrA dK-;Fe4Z7HGe6NmNǕXݾ~wFȣՑDQE 
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
?hoXQ -wuǗX  |ҖGϚān F ٍ}wY-jfQd¶~?#_QTa1bwA׬$xՖE*ASY
5mLc{~8~/ GbUn|ͼJln:џS>&0Ӯ4i&U-c
|}7?i}bTŌ_\~ƞmmc]a\vkI(Am?PϤhE#_N6ȂE_1WfDW^5UԬCffWGrN8#!~|̑gFGnɽsOkO>8xV5)֯g5	72=+3өNrS#'#
\MnDZs$k*bU|mǖ>g[r;IU -Qɭ|K!kmƘAzI4wdS+81K֒K;vgYXk^~tVǵ(SK"ZSv~~~њ]t^2c˵>Tf#bnzcߊ4,!7[I0v#{x|SYC:+q_?|'>!of:?NVosLN9Ca6 \-oc/MO	)W̗L!,|Eo{hY\0NF8~KitO_~~~Q"ijp,3H#bxЎ{_QLt}	 m$K?ɫEjd &E?60zgM>y{"M$vm/<ES
^u-,X2H7Q:(Amr@_*εܛmU VOf9^u47.F5> ]~G_@W~_Q i7}ѵ$:"@܎tG?]G|IYcZ$nD!8E1SZ'lҼH7G9uqoohū,+Ye`A{w^2fO$0S>Y85fX680xI;ڟ
?ࣞ'ҦVRY#jzdcHo+lmAɉ^kovgïj74۩GDȵEH1f9ݐzĿGχ>27
>PXt2560PϜs~UσP~7v#lc(Ν,*8}d)eۧmOoZshtg-hInW(8W2_Yo$cq+Ds7.׈~(k&iKpftB5d9f"azoǷ 
k
7xv?Cڢ_X	{+p!8`D | TЧNmJkhR	qߪHuk[M+9fGSc5f9˨#sv-|]Mֶp>b6Lm-ёeW+9UaP7'5Z۠Iݯ%ZKirEЮl*oA XZkPJm[MK[I!sl6ڮ"'jcK4vp~gşo^զKYgEL+
A5%mh-װ[{53vr
m{
\h:$dYT:|z_>m7^ץOYZA8kF
K%~nAz5'(MZ݊52ѫBo5k=0Y,g$gP=}eX<O[Mm&LN#
H+-#_ߌ&|%OgJHXOa7<`64$״
|Q8|/{O\xC341Hdehd5 c8V 	b{X|.ׅH$ʯRr䎛zΟ;?h_
wP u}  jÿj ecmRY%SLK	稯	"B DE]8:2jЩ4π?jlY]7Uσ_^"=NF[I)Zccu%ISe ϗOy쉥)Kd77BBI
+ݎ	;.ewo>/~ޏo=U4iVlY'C<?<`n r g)^s|i]Fdz),gGXɚhʅn]@gf<G£%Οq}gugt[EYs庍QiJ3+;Xg]OA,_<+}& 1\\j'ks߅>F|Nic?</f5aԑX.%B\sZ^=߃7Lk:[ Eok}ťjLjCYwe$_3PKٞ8u6>RUkék3Ú׉!oM?TxoIoM[fĒG'&KywZi~:_wӕ#Km=J@ cZu|;&J쳻 ^c +3",zPhf؛hBHB%C_@xw@i&Siٗ1^,X̍؎^\3@rE[tШm|D<o𖥧[jԹ eKj2"+L~[j z{_o%ڮg[`	Q#\^cQ@?Cm/1A~+,4tTsD_xv })V,\~w8qS^ݤyXY7č	{kfo#/Ès߽Mx2 o4՜6hk$ci$V$mB(6m̒ QésƩ7qfՠ77֟Ok`87;5Wr
1..s^i@I+.Gʂ{߆k֭/i33w\eu7G ;$N+/L𵿇mcqs[xbiV-[cl :> }|@4sŵ+-
 O=+/^h7u
S7Y}[M6ỹhJ1ӌןQ~eoCUh}O ࡾ "𮓮^Z/Ac7$bU>
q<OL|ҍ'ꇷ:mЖ.B,>t_Vi]wwW|6k<ɮϹ˻c,y'|_a
ơqhnp}uQҒp֗4ܻ>)xy5M>1k
RO=I~MדhΧI4Z^wNvuOb* 2O"+z<M-JMFK}2L%9R|BǾ.^SGs;}mZx^0u+X&AiH.(2c$@E UaxgF
ƚmEN7<jWcg#sOËi0}7KO5<M 4DX@j|wGRw?0c]xSe"*#PA 2dqY^kifa[rGzw^KW|CFʚ:uj67G\$VNݞui̙Nu;>]͞[\jZ%u{],qf<n|7xn*3c-t˯ڣin}>lRyzc]FJ&ϺLlcH"۔e5y='5U#8>?g%	
.NFqX^迲׉.K
Q»x~CZI6(u'_xմsNau(r1Hʒ9^x#D7E'6W3][oe;x}FMi؉v&ŗ᥸wwjc;'0:m;djwPGO_O^qo0ƭz<3w;m߳ʈT4 X?M=z#KYOدJ*	7Mǟ)Կ>4xGǈo,ZOe|cJ7z=xfk}>5!cV= Ҿtoο>_d];^{M촘㼅-[$=ǗJt
UXʣ-&`o7Wr|g%ߴ>>5xs\cXB4tGu]ÕU r8W4^?댰Y44xr]EfUб
H	sQSW:3<¾6V46=R[lylJANoEwfW5~W.gۢ
ӂ8n]d'5O/6$vz-Ʃ$zzIL3یFʺ W+A^%ͩWD-^|_½
{i-zz־ߦ~J?8|Z6mBlq;3jyi#*Oh>(Mj^XUw
屓u5+7ʿd?ҽ77Z/$,\{9q
08u&ޥ7;m&t}fU! yTh>x鼏iO\74[ՠQ_>$1$h~I,~W#'n>ԗ?<#?Bk漁N U1%ڪ.H#BsR$׷S 	gyp@GGA_M:mgA59n"G%#Hl:zׅ 
o6מ.T^K	s$y`c]Q⷇Q}t:
5Y#eݕrGJRS.5?+^Wn<Z~c!nf^GT|k3M.A@i V3ؠ~~7J[&k^$FhWkWrKĂ2ܪPH_J<'}a;=6~UڷëiO'Wc	b.{Շox
|,gofyd_0uZP']ee7P{%JBZf9km? kcX?<m}	)-"`r!(`jWfi
{83aN2xֹcoF-]=3+|+.$7:e伲o2x5ݟ?Zj	;V}kGY\7?y>L<ٵ8p<ֱ5ΏıƃacedDv-3c:է74m}Ծ!jw~(xm>;c9WVP TA"t{t~h~<U'tflbckpr3g=#UfF-T)jn̮6(ڣ; ߭u^"z5^{`6䘉e4Ô
y2vq\xz=C!C4}rS~Ҍq]zֽή5+]gM>"mmb|o<r@
>|ږ#M&xd4ϽpL̆G6EKwkŵ6@_M>2I&̬\uڶ05#;Mh'PZI7Uv~v9B.F
8	}b7N$Y2Jt>>Mu:mwXxZKJF]$6LqNԞdo/kXDAZpN}]Z+ Dw q#x^['6w׶ז^"=Zٮ	fNAi:Y|]a!LM+#Y$I&)W2)U_υ_C ^A_}ϮAy$;)0QxN,Dk~Wu=ymc$(>~}6fIe!y?+~w<Nsx{Mgot;4W`	r8ax;ZM-2?S%o
;{Qo
Ouqm[^uo$vۈKP1_2_>5xɩx\O$G]9C# w?b+S2L^ݦkjѮ%Un`LzVn<бicG\.T*} #̍,c{w~ i(k\GFMĐݻBWI *n4z}ٶؽ{ڍ=-EKݳӯ$_:hϝ-mdҵuCm0n mT)x:h|{oj q2zzזQXd?nuxG[dJB&A(A{^y[ݬi赱nEB/6?Z/g;8бX*7rOs[_~ x Y zח
=GCVЭ _ݽy~Žan
 Bzo`?QZGvA4Rm`$a9=6cMnռa
̭'UUmt{Gmv㞡
Zd;Djr\n9@u5gƷ#~KXF3e9^-\\c>{ h7P-w=Ye8r$n$x
] 4Y_iAkavf1\d+:ð濜? xP[xnm!?1־ qZԴY&澼,cxۄ)
Wx!2?fYܧ"^|oIծRY{' %hTdqWR.2qg	)GGs i((t߄P+81ЎikSۊE;^E})אָ}V¹z4lcNETQE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE Wp~j?(+>[ښ В(hGMh<dUnm}y8
ޣ$iw«jv[nߕY9>gsP%JfQQI*"Ҽ-m|*l$mPpr	=}
-sV݌"`iIY`9xE3ѳ_8R睗P(?_3/ubfSk۩<zfsyP&YuO4GW忌g
?㇍4{=/PX>t*]kQ_t{8<DkgƖ~G\@7$lb0{V^G#]|c<Gy
vW0i
d,	 rWkᶃú]i;k[RnX[gN[&Oп?wB7WQNNgUlU| ou&w3dN繿:U5R5[^>
}zLoU_Z+O|au Vb/K͞{}  3Nҿf{k9"yGq:&0קxKQ/csɓ W)8n>'6fwSצr5Io'^_&;{7ۯ אTumfygf/:$'bᇃ'r'*}dg>?U|S<u
} O$;\%b:fO_udqG gOv1+s5ˢ 8Xb .$xR9U]nIʞ.n=Y|Eq3mG=U4
1kgWI 'Y5;)XtDeuDפ:zU	66: U%N-{a] :,Q~R|ݮ9S<5`܎HWFԟln gRLm1&?ua)Zx;+2F%6-M?>%To3TsXj߉d]o,:sŪBkliyz\mqk BR  妟^=єGk^+VJv[k^'JZ|; HS]5/5VK][mc\7)sz{>'|F׾X񱿺Dbtb[ieQ
.K; -;gp^6g08?JGG^%{t{ >/EMCICsE:I<;aF MI
uQs*0+h |aǷ"UA?=CJ|tY@.Pc{=w_^1^E[Iizu2w%zc({h֧w9~ΞٳXlMK~,2F1FxKǸ _ɶ?\[ڟ{ ~8⧇Mk[%fYjC vbysx9u-ʖ9=E5JU+SR>϶_$A? ZC#X6K٭yJr9!ھ[ms#+$u>?
|y?xUo`ณPYcy@ڲ c-Qw<ʛV2|PYjum0L$w{ j i\5·i5RBXfmm FPt`׼g]Y$>U^؜mW~Ϟ?ĝoOtXob&U.hQ SVyuku	ӄ|}[Ve峃'sg5>-OSmf`#  PuU,\?RuR\_ 8k6}j7匛dV
l|ASWj=T8'Ϲ-zUX^,&h$R]5CI>vϜɮhZNla<6QA<1.vT8A'~f ]e៉=^6mG<#3_c |
&oui};6ТE|u2KHKS9H\yɦ1͎QZI|Ҽgt{TyGZ f[]GȺdiyk-o(< s.iִX4佌nGfcfM:Sj\y]
qXcaOR۵tNh4[ONvg] '򯜼_(q{%S^6Eϫ~	PgWß
ݬJrOlgP o
		5/}1]TqODµ+ƿϏ<%wkkl͎i|27xZτ}{f	).(,#Tm=2
Fw_tx7P|i\kv6nRX%sҾ~۾>.N7mVYFdhNq+c:|f#nz*Ɩ~`xO}?Vnu圫6H =k6i-7y-4𘦹^i%@ #eTԵ-;Vqw=PQ#8q#|=+ڷH/O.~ϪW7^X`|4FJ9 ƈG~oK/cj}8}c;fxL$a[kLUD[ #<⸏񭶨$mcҀ9? pZ&O5ʎIc8_ 㜑yY^&tH|97l/,:バOҾ8v<> J<?Uy%ѕPu ׯ>>xCP-t VHyI%[E'ِ#!@r>U_\-$!0!_(?7!^0Zs>~J|犵K{ۋv[{&r#]nTH#rBƃ
J,n^Kx~8`3GkiGouDIY<PJ6=G
%|,Ok_IdQ	gc 6>A$XQS[SxzjN}>2~Q~ϋìCwgkx7Qyo 'ژ'Ǖa4~Zxo~Zq~$Mn
g׳j0ֿ9->Kl䐲c>:*Z[Q
O<qR}vWF8y{w&n Xx~KosjaoU5O+~KV\)*-I/ZEjy75~zoXrlDls߶1Z
8x&J19#ipLB:
vi"nFI?.l>
G}
Tbb|R~5mVX6ZI'{	 |a;A3*$x~R@EG*->)z1W:^^} m:jx7{#+<?{w½Gic0CFD Mqknh_χzMpT:ύxSiu+_l[CIEOӡm;Mvv5Eanqz4r>%M%Mޑ=:=?Q״T	$mBAKpsaޣ2|J<EcxMMU^4@k mm?cP[4:;tYXnF1pkOP|S\A5k4sZ?wTUG*	>7Sg*J楪$ dx*iwn $
߀:t'<WTZ[-p--w
2 R'i="[_-$AO]L	Hx4/kƏ\ɤX&;."2g9CGyzsn>֯?o#VUdRq);V1ר1?k>:?
 7NѺB('8yVϋ[~$/-ޡ5;ɖAaTqiEqď84u ZRƛk
CO>;`\#}J7m /yrI+OF׵}?&<a4WOw^z+rF<,x^suoxGA\d joqi]\Ijˈzr͍7'zrF+$|\!b[o7D 1néYI#t_4
|ytz-֟xR[XakCa-2+_Mn&r#]zՌ+(t;9y֛j~
ѩU}&X\u8
zzȏ<cyt,[IOcrѠB.(}!!_/5HtN<A]n&c.G+
裈ucr>~y_xo~+gȆYEF%cTa_<|W |'BR|?>-Iח0i݉;d`O'< ų&[S[$\HXb`dsQңx>Q\NIZlWQ%5O| ^M.Wq+D`ЭBmOIktڦ}kKܽ G%^VP[ײ4mc=z?֫Vr40R=ξ/TW}v?dsg ?[Du8Ż> vj?KWc ":ii?s![
w(kVev`RKtn<1H-0]hUPFY dR鹷O~||7[Ei	~Cb%,p#9d{:5fDH`{F''N"+CS~ u ˔xv6v6&_ZM <}:3m $z^ok{eQ ';׊b{)r=>~
>DͤuQeeaGO|y T7ֻ2nm
:ᱷmr61;׋
=;Ǿ45b["1ف9`<5/^~5{]FTi㺊)-
iK3߾I9;+i^-{L<i<cR h6kHծ7^-:mJ1;1h_KujZvHWkyv$c~~a57 ٗd𭥾[$= TXX* 
WƏEoxfZ7J
ہZy,hN7p{i,Vz֜J~'j#OVmlauoZM۽vLgw[xoT `+t`A(`LSL
xÂ_}Hڎv
/-Q^w_)wNt yVvp0[gs'
teEfͤxKzgym躅uX!l`:ǋC-xzEDt])]ԭyVlУ;Vi>bM\tֱ. D^@_&<CW-|;4z]p450-)-[յ.L,_QץE$LHHIi4kOC^'j>*Ϯj5mRqNٮOj-ḵV7}S^RTE9sI[ۏʻK7^;_O-pܾˀHA7P>$WRX~#Q	<gbOA6E5Gњ 	g٧Y,k$iV??+^kRo4iIe#=kόq@'46;40޼'W/T6'ynU5*nb20
Һ-%{#ؿf ûcK$J¯F
 Yd.=o iB?xHF:{N$
?x=wOCku)'XhxҠ>S]Z??]Z]~.p$}2ɼIp(՝ka՝Tp5V=7ƿS_	rVk_ v~$>E im!'?Ѿ?h[k(ԗJ<
/IOӣر}/AC5MZ@`!H	Gh+
`y,: BVk~Iz-$[fUcj`y#.}){VG߈`ׇ-Vu|$gZ3Zl> -6|%i>,!A+gd,W&c>h ~AXsa'JGjXu}J_ZrOj k'3qkK{?{fby ԎI7d|]6lm<,=HSSS< u	#D+U)3B|z/542hX$ɜ{־t?K{[p#C<' 'M^>>3Fw#MCusco?¿پ<-m}o8&V9'=K
 M%G4U=j+Oܶb23&'~*ISy4Ѝ'n']"Vv]pip)sHCv}{;{T֦dqw&b#<E8cǩҿ'|M'ʫ%6@^J\?bp7(!1{ܸU(_/GL_ebϢ 
z!ɽi. SmEsPNE r9>kS058<뙭=6D>] Ӣ*@( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( J>+E_)"ko"Y+R@*rr AJJ*LcHcqk~1zP94բ&+'>3lS#VfkQXzlEIm teOEmn\}R^ۅ#~{ 1\м5jHlr_5jf2hٛQ黣
ǃẎHd]PIbvr
>V?#HOx=j[֫USƎ}:+u?o6WU\ps.>2gܑ+xZ&wG	$cceo\K)O,Evpw1ܠ$/c <Wk]6V.o+KgU~nއ_|7 muז*xR4q1U#&h8,FFIg~,+ǖ֛)㟲OT7>#sugo.Z26H	?uv>idx%?N}i w$<10C&;);`6
zO Z1+J2h
3Jҩ{4#M> wΓ~:Q颃~זQ`uçmXO42LFtԭ㱸C%Mt>mZ9n}j.k)Rvq7g%q׺ Z?/:V}FuޟD^?Oȼ?(1YCj  J/k~j^2c_j [iLֶ 4jd!JQMKF\XY^xV#&I(#,0FI:M=ku[t3övS˲?.Fe
f#NkM?f8Fn_5[y!ݎxX<i#jMiQI:2 bQ;
᫂ΘKi{]2<U^*[ݖb[qxkY&[ UW@\x%&$s)+TuOx$7^%$ۨM*Dڦ٤v*&8o37:Ǉ)}}wg Qf"fLy
?
&8I˹Gjh7 zGt?gæ_Bο?h>'x*aյ>?e7
s&O {Xgz}ܑjri~;rCDp sp9k+֩ck_xOm^!P{M[I ժ/WH5E[-|$l/ ہK {
xSQdݷڮ oSy^-+z7u]7
߈0 
ק|tu_^{ȷ[ߌ ^<;kl.nW
|KvV{[.滆5x`k5x_KY7'B;osB&u(m-VYa[,_$@}~&' bMBo?TsT_uc'Ŀ^xv8t}[{6IR[X!eFkrh3[vll<AC[ćHW1(U GWњؼ[}Icyq1 Z7a>xqi.V֧S{{=_ği"Um6]Sn^ǬX;<ʹP^đ?VIWĞS	ڥ)ŷXnZ'q 42XuvI,־,]yhz
R>$#\m^wdn zWR~_gS1S;>h
nַM,M`Dʒ7c y?#?"
7EgAEºd{O*z0>Ww/#\{<,A?~VY^lRL ;xMN-mLs upqo";:^c|ggqȶ6u+=}N}M~K	<a	_xrAմr mXV[0,W
D>`eK`1__ m
?X<k6/#W[Aq8OfE߅>_XB׏S]ZaDF"e$7z_8D?`ڷOX#Vw_9[؈Opl澰Z}SN!Z=ΰ,檱(pΟ,o<QqaU<*oJ-ްݶTa+IF(1R> VE|*2,W35[H$ኟ.T_.)Hll>o?_vdk[^,lU&	VVPFA53mMJk034qJcPx=?x}x&p<?X5麬>)֥/lVu&WjckY_[C+ϡ<_|O˭'Xl.(0Ѹp8'=pk?g̱9Q`M)ܼᏅ$s8+kq{ IɫѫX/ci8 J euρ)?=8;PǇL$xF nYFwtቆkz4>vj!8sh? O|p* NZŻZʷ&ebʁ;lnlqW+^Y|Yc;zkYƓ:ݡ`)VV</ڧR~/.j_ȴ$]]
F0s]k'SiKiP=sq7tO	64Wׯ9X1Oo|eKKUkxo 
2;{ V {|'m|jZΠpc}SË_:KN`u:lIӯ^xum..Eue]L71^}^jW:nkWO)hyek tl75+v%asgֺ+h(LԱ"D r>jFz[cYx7ÉjM)k "nt
Wn[|ɮn(aKya0nCle˜@W~ ~|$_/𕾗5J+|iףАF0A" hk[RRxREʲqS`^wU#t]O
XOPVe?y.߆n3OlF1^kԠԡotnc?GMr/{~~O	_1V+@+ӛQM]J-|)g>=,;h29.Π!/6
*߁w}bU+[U}n35)no507'M(s@~^;ZTa\^.% pǽ}:qybQ^NG{ߏ&~~-3ximvs1)n;<==/P<?֡s&#vx/(^M&cr$OCZƻy1	ϰW5<_@-f#σb$jUq4<#|/W^%3;FUOGx~&?Zǩ5\˅$FOʜ㝄׎<>-"ȱw(v==u8uBU)P4\~8q]Ԩ8 r*7nl?oXg_^myLu*[ҒV?W=Zӭ]q W tٻ:>3^KV]BPON"ivi6֏iV$,#;rΰUm)%G}J_o-LA_ƻ-3V/+Y!էsݍTXv_	:
ͭ~o˨kWUx\._f 2ZMi~ 2zM{	?/m 4a <]1BAaQ/Rww~$6:]֑$
+_[՞6f
dCW{׵k?Nsxg<;DU?mƏPc,+|W?<Oşl|+JyOF&}TCx~}
{Y<K=%ۖ=BX:Tb1tbc|6~\hGK
3CJQwJ0	S5 ,ůuGcL5E15ۦ ^Xp|#ktdi}TA#=tךBݺùpsqZgs{ޞuvu
VZw}\]^^{L@K;Y$`ꋷ;L- |M/oRț[a_I~WM
-~J9XRj:CRWWd꙯mzKl
y/bqqn_z_.% _Q߇1Lߊ^%+3n
u q۳\ikl/_$.cXȱj{|&˿LML9K}ʩgFo[:[G>ebJ[cs|vA?MdG`{m1+Z{Y.S׼)Ҿ̯$HAIҾeoTb⫸ql:z^-oh;OQ9ҡܯuz.fO94 @vN98d+u[J T+}Ce\\xvCo|%|g5xg[wW8'<{g=^iT]>_f|>?ĭ
m hp8 +MƟH^xC\>Ƶ]JuOWVZH$`voA?m xsmƋsxP\E}L;7 JϯJONR{<5\i.]дkq
@& -'9PG>ǚeޓaUI&Ruvmq*O^/\?
 gklkv@~i)|ۅr H:׺*=/],ŦjjVfs1~38ŜSu.>|}H|+M׵Hn=w)nmEU,@(-wj趞"u-"mJmoޘϗC1xd^p ek_
u_譬9o$4Jo H>V<g5-Loå2w?FVsCD|Ro⋩?50E}	'DL]n
[vv	m9T!~x99oW'jZ~WtpwE/ `{3yKtBCyĩkk pA/'z<`$<VW#
uuK[Ͳ	%/Hl@Po i6X\hIGulfNmYX6(ҿ  d[WZQI^eć&I}+:~ݞ9:/tˮʷU\}"mڌpHG#A^KTSӎYfO MSR
  ߙ88=?mkUWƝziz^⯎<Axė:3)@oX8j3~^$*}&WN.54j<}` }W
=|/%SS]CkJv=ݪE{nv'
yjo&s?>wS}RVSt[y22 1Fkko}jπ 19$[eEрBZSJi+ ྄oWZ
oA!5381_
5_xcAMK[iX\G$QHت1v
>ndv⫛n?Ftz&L~T3ۥp	hlz55la(mG߲6tmpt?j?5Fm`o<O֗f4Gd6w61fTN@l#~< Ŗ.\CxöRypmUNs:W,j捬uC5'm~R-Tf`\ K;YY̡#s >,K-E?%%=ۼ3q>!cN NkK<T0aY`O ּ'JwL!i U"\g |ymZGt٠cn-5idSǘ6~mi6W-Z%E	o`ڿ`e9֊S7Ft>? >y}u95K6W3h𠲐J+˾|8ռ㛻][K4LW֒H	+"#濥=GAmd{xe(X mM7\%Lޖ2Q~50yQB|Y75֧'PQY\bE q׻| ox{')T4+8v #skk@|/+Y-.MVO%2p88k;n|p=7c?V2#ox m/zu4WR]I"!U̒<kO =yғ:dg%0;41%:u dԖpiGB袊0L p b*GO
[F袊
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(
(+ak2M[<ջNi,cϭV&`QR.?Զ=+OSʌD~\GP+>ᯕ?mB?5ɄU
쯨y43$m>o0 gL D_IZۧҷOԒ(G[<r*#^?|?W&_iumҏ߳*ƙÏt \j,j7Vˇ]/WEEEmg*
& r_  g\k"ͫi[6ylrAm	Ȑ
f?U>i5Y[˾e# >cjb%oS]u~l~Կl~xݵu;|&IQdRVak_e$QbVWR~F(3K4U٣~#h7s{y2LSNT8ذy_c^n}% yW\}\o#c#}Oo^-y积5YyN>Dك s
]|zGƆ; G
*E0ZD	SO=Vt E͡Mf-&H@Ok%%Ζ6ICkWY j8э[g쑬^x6*pjX.&

Q'ֽZ=Wz%qdڮ]<7co2K]:4#	Efvg-yx5j^ʪѪQ`qy$hi+9RdB۸1=Aܛ/3_CBߺm#j񞹩||<;&`BC!b'1X}MoFO_ing,Ic.;S.<em-ZiI {vdqW_xqڼߴ^M=$Gz7229mg
jڭýnͣa]鸌<1k'~6[Yo+]%b;	$g_XW%֞QNLgN[98
>\j~ҕHz!\a M5q;Qkjw}oy j~!źO p +YW<1u?I|[g [?[W5T/=:v-
KûО?&i:Iz~Wޗ	[e x  kqINd
20.gI}Ønq^Ox~ۺQK|7t|MFduːIk-Ve4ݸK?| {4^&e:0J>m<`[owęĞ#o_]V3uwU_26K(#״ ]jik 䴼.-grc,R 3noxZdܲvb5_K/&_M<g&=Q߮@an?vdpppN}Ԍzwx,Iԏy/%/$zP7O-ֺ^CE Ŏ cxh&]X?>{!w/#<޹=|GQicJmJLHs	>E~~6͚\gg&1ǚnx=HliK ?Mǧ,9'x/GКJ1fVdH\(.g$t*kWsP]CM7:?cQ<d`!F
~gz>%|$7i֜I#DX:T~ב7)u<gt_\ڧFmm-aXȑ܄)H1p]HsBƇ[oot_XoOch]ɛ'5C=~hsKWMct2Jd`dKA;^64Y6K	)
 R19מxwHV4[컽	i#(T]vȅz};WWtcV
O/y5rm!$U<^0qӠ?O Y_4k4c6(ǲݣӺx7{  ~x;kxCv׆!,繏uݾ7̀>c뿍_8~#׈X$}9$mZ[D	TB.pyq&znn:oŇ>i֚7oČB't 	~Z|Wx[g&
Gw[nіIU/2Nz  b	~'x#xcė#+c݅ݫD!h
 F7#]eזi֭]4fH"X%,GQ"mc=EqХVNԏ͞G <|_ix2^zBHtB1]-7vOk_pk_cዑp{fd(	1Ȥp[,K$eY|]J9Ɇ1a59ZWaIyPwZ2<z/#,63j,bECK~+>Zؼ3
|jM+t˞z5ڏ
>t8xȯ| iP MQ&)bi5xN2}17S4=+d冓-ZjSY"_GqmI ʅU &Ug$ܕg})S?⽌YnO¶F<)[XZP*QT(bVd~r [O߰M3 ޅIDүn%$ڤ|;608uFOŞC~j@vH<Q򱟕i.dL#I|7wtj[$=q4ECysax񠺉ɚ]YW?
|fE}Vm,/oFyd\OkWy^j,= ݚ,g̥'~-<Qg#ՊCFF:Wx?~.yOMٸaPGZԿd+-<W[s1=I'z fj ֎a
$ϕv_dVKKO|<zwy6{;ym^I4\c
k~z;ʫf?h	dGYK-כMwg<cM+R>ooeGʷ^}lxo	Eak6(88*w'ʣrY? {fHUMmrF!&iX| E!|`#xWְ ]t8bb>vI9'eYCZ	Rw+Mo x6g{5V;=+]/^K%wὀM_UD5˽E}dd<D^[𢯱ʾ2oxmwY(\=Ec,]GQ; /ďZ#Y/|{g"ˆr#rѓL/|,7aXT4AU}(u"gc s_u|#cmo̿kc,3}*fiO,"1>q ^"pDO$yNntNy/`kŴv+̬3c*K~"0̬ѴAmObL-|8oo]Y&-COw"mpd2NCr	1߳&|mjW̚'h#ԍ
[;rAOW{&	ܧɖF#t+9xŵOrR9` W'_ _VMCG"sg,@vW<!8+拤}&4wy#NW
èjaї,\90/
Zu&MU~' =93j?_?k1(7{Fk"Gêxv5X^.S1Xd|8=Ez  oQW_{QW7VL3!s\:[8Wҧ|KWѬuG"	Wk(5ȳ״ӑ\/n#GhsvQ%^ "-'.Jt[[v<$WOGLt9l|E֭jf{C
IM_M灼&}}%&((gŀ}_ucbg*;rrk?|"'Kca3ϫN!F\ዒ2FzzW:vGM<P/>*YA^?ѣY @ram܋HYkI1Ϸ)#&8/Wܐp	.so\)sqN}9Jph
z!=hd0! W>Luv1ֺ=FzjhR> ?h_iw*rVK'؞M	`V;N!~⏌eWuk_:]񴱶?ټ#YePU#'@,u}Od7i`>̪TsN+o[7_/V#{vpO_S-?g[|1]wCInoL,$RF;Xnâ,8V?jJ(+g?Bm
ͨ_Y>6q_Oo<v< d)bFOJy>uT4+?+tB׎||xKJ\ ײ|y8[1~/|3Vr\^cw-ԫk4@Q33T~=|d5-d[KO3lYwNAp=h~y&&x=A	4X]=Zw[ß^:kSIO$h-jڶkz>w-WM`sɯlGR>?\5}'A.&Oy'0D c,<[@諧G{Ir'O;Ҽ/cjiZŹ`Y|ąD>fѓ>^1|]Qϕ
|#~c61 Xib:lf(l&@z& [J1͓|UmxxN`xrN񝣆6G`g$_4'"{]3D"{XaGFrt8u>XIzqQ[</%VE{a\텥E}Y
Q4giKr5t>x=Żm%HdZeK3s## ֿ3NoGy
*/Yٮ+#
p9#X)c|%:-1zܽ HdQZ;k\il&YI=[<mt#f
G:'&\~1H*l=B<?#[ xE~G/VfDtz:6o~uZ.' ,*0_]N[>r}85wGC6[tH"P`tG-j*J
0:O&[gX_[e'j
۩y8>?wM%}l`Q_9b/g?e
%}	+ZU~:(s@(>'5_bj˺36`-G4X~4e2qVR]³: W#;E6Y_$}jH+`֥5QH
 tԶv t6
W@.Q@9TQE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE օXБMuXEX>#[eƚ1*(CSvi\訮w4Hjvߵt("	9M?ms'ovUW_<O+c9OЊƿtaݤWG7He{O ucW\ZGCRZ(ڍ"mY: =;Lң5ơT۶:yψ
Z|,^̺ƥ+䴺T \1ӅwFjƍmrr>/ѫѝqӂz
!L ld6Y_@*~G(#,e|Ptدst9_5U4k ,BHFxɩ6qk g/fMF?'	G}S^O%k:*Hn;ASOu^}a	GEI3c>t c
t
iX_&50;VA]
I;Vx؇¿
o|?LӴ ,`[[ۂI}׹E i
P:m􋀧	ݡn/H#|+2Ro=Ğ
_ݶg>;YLv	+{3~מcP 
ǈZdc#
*nnN9vd-?ి
|1K_h5l
.d \1E|'#|Jk|}Ym%om.wQO`zȿ'<Ejo|Ʋ`:o iKPK/brhgCT=+ȒOMZ_*-Ctf#G\|wks7404cg޻_xWf9fg7EsYy?_.-XCݥ[ h͎sGz3
r
ϋ+hn/uAq妸~ϣ ijڄd7إeِ |.zg|W4!s)
Ot>v㈔ֈ==6GEr> FX+>65w?v^^w??W<ԣ޼2]za޽`s/k[0լ1ܫ>v@7= 3g1|͏tWxfP~UN΋qnǹ|i&laNۧL h YI3ʼҼe ,n
W_n sr}FΨb{oXO"ɕ6P㏭} Wľ8l`I/ُw
~x?~ -|QRF']!~~ htȲ<j/ Pwv'Fw莩U(rjk~dm
$ jO
	am
m5[M4 jEŌ	²-WA<a)/_Zn%ͼ/*jwX
 `1W?Qxkx_KgԵH,兩uHeDYS/8 Z3U)ʟ"_ZCv&5(4W@~e a /ֶ{}:IiZu«}ő+֝qo4BF]D+:g_I?@SQlD'`LM
v "]>4_2M/  Fp>$h~0`KfFRDxN͈2| <eb
.;Lm4#33+*X|?xGx> kڤlwxMFmibN  Ho_ao7ݞgaiFTِ1Ituv'%yjvԺs}x{}3Qi4gUQ1x %o'nϒաc4,'q*#8y⺏qnF?m|)+lϫx6'}&`zg3_pXx/
"xr(9Tڙg8̦R٢J#>pI;iZ)lK LcYkaN@~~sKxQmu,΁KODrƿtC?M(#^oc1FY6Fn`^hcoxM՞2[i6_*6Y}L.rκxuG# H|;oŋOUNO~V'w渌p?d=;
X_hm-ƏyVM:Ao"d>gOվIcurlo>!xhK-[/Y!ۥ^"%#^K(lǧ 8<TlJ.N(C_ 1x+q4?4[G<șW'4W5w{˸.j>t[j'5	$HcYU1>V8W__𕮭p2<I"[۠
	+x"P5MaUj3;$X_MjT%UEu?? 3Zu>h$Vi trrGZB>CԴ}FTo;w\Z\$JQe$w?|_Di;+LQst3  oZ>'/6׼]Vռ:nz.,u{!KyՖD;UFj*30Tg}?6ZDWReY#N<D9 ٓ^I.760[X䳉L-ةNL"xc>x[O]&Me#2d W_^~Ϟ4'LYI{g5u'[F7x72C4	!eY|>TjT:6v{JpyK<'
!&x'Sŭe<i>"O,rDx
*pF1?Z{.WƟuk?g	j	 AQO>Yf,^(0>q%G4Vue<p3MmLZ9z*Zh
5Oo hK:2 m,7}b
9+<gb )/mǊ"1᳽Zʨp AGJj="E
6a?l$Y<D8 p3ӊ?W:E|K?ǜ-zYN2\d)fTa$ C?j?kK|DZ?yGȈ(<A
.3ھU{iu%Ԛ],+̡9; I'޽B8%|A	 nT~%Eiy
ĲmhKtֿEvx: 
[Z4% } 副Z"[~;<)I
rMyl_L_
cyaθw]pFW+<AxGnWij&V$g޷e&bhuo'?OM/~:jBM3T_^Lt}A<#
wqw:*w g83YW-&'d"7m	1 w+ |xQu_<4
hFt_H?5tc9j7$nD/ѬtmN[[DB$*+ gxa^4j#m[
S>SRfvX*$7X?ࣟ	oi9itNmyiFYavT9v?F8 gWH5
ocTPUG`*+ݕyéZƬV W)R"Y,ǸI5}&ObՅ؃;x	|%}KmA$ITr	D1Mv~NQy50ĖWD\YH֦{4KitGu+;
jSߜ48*p0:V/¯'R^au;Xk[KFQ<$ܬ;^ ܋.fHWSL%&$]jo譚H䘀pG`ݶz,ԚyUy͗_^7ɣjSB-{Pŀe $8u>V7iڮeY"448'xo|Tφ&w:j7BooFCG6ww:gⶩj"m?INq+4+B4RZ/S4z=7jwKK)uʩOy/ڿxKZet-
?u"U  rOS_|OH~6":+!/Qaշd;d0šR<H&Yz]DI"zUq-(~M<
5I|Q
-+=3{k[nbVl_l,Khfm#_4(B}QOxzux ^6<A]ܭ]ء1Q/E'$+k
$?pGf")&5ҧ'#?~Uǈr7wcE$=/~:HX vmQmtx/ÛL(|:΅#bY#YZP]r33yEyW-G#ۥGNܪ_D~_i8 OGluo_qjv.3fx\ |[7hֵo&弧{il?z:M c9c\O\]pC椻ba `rxߴMA|@u->Rѷ&o$(Z*U
IxEjoO;M5̩f
$5TJrϞn)zns^(t>-ZIK8w^g~<FSo5+;)4leU:Ks޽mi^MQ

x>M[m2,&˸jӜlޝ+_vzW~1x;l~Ehn=*%oc(TT){!zڬ/
/knuMzHY/t_27<+9BU{Dj?)=5>c X 5jxMXͭK[r0g={/LëO@i:9Ud| 5n
Ck_/VQP 8q ;J9uG8`kN5=
S,).f?>^YJqW<I.qanW[QEi]\)
~Ad-~O 5	<Ujz|(>jL3*Q 2{/4/?s\s'(|/$1tm,gfş9?^Et_+/fm *A:yz»/3t~?5=8hbI膯?>);SPݚu+tu8Iy1}~Ӥ  WA}?5m Za («_Ύ m|r$gAᛆmoxE ܱ~q}[>*mdLi׾MD3'}3_~,_¯Yw$#5J:_SK*ᦣ3k
6f e/с"Uc/c?A_NG9u Hx( K.x_<Gc{kx^U (rA9Ԧcr?!Λ5h6qfO5ᙴi6E' ѬlY*36oض>Cz>-|3~ߚmޡmXV0K`q\OÒa+qa?
qR9#Y	koj>?>VKO6ӟ˧57aj6{{$T<j#.
r*/S@ZH )T{*<6id@E_N:TepWRS>֝|hh)6TOQ\CMzThp@\imRTQE QFqF (u QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE_Q}+ ڶ;mdullWki㺞ɶp> 5C|>-+f/S}/`m_=jH  ǅ}	a&uVL|lQڼuYWʚ>'4fXߐL̬U9?gBhy1~O:}+~8_	[[퐠QuVgb*VDm(cH4sR2R.UѺJʕ."]0֟(_O3GX hk1_fO]?|FvOU趨3J?< .#⑭WV*0{V+JW:ǅYf{g&qo Z⯋ CyVEX;NGlƅsyɖhP͑Gnòsגj>2Oƺ .8 x&ޔ~V?hz|˯W	e~^^M. fJ +{ǕEе.?2W#3_|v䍼 m<^?+E4Q~$ǧ-[}oIi!Dg4 PI5N>woke`UUO%kem&wx]g8-vhD{_
u2mb~uTk(qTR]NYOEr8ݢmԃLWsɥԡoxO~kƙ ѴXFg5ǥ^\mmߺڰS7X~&[#ci<{OXj
apqWL eVC𾢗"PVf<O Vr\i>MX  ΁e޳Aٿ£mY2 <øh;[ccQJAԬp-|۽;c?j&/Ow6!eYCuBn׷1"z֐DsMxZ<5oMiҽhv,DYWO}=nlhXy5}Mlߌˍ^ Q*{d㏭}khGlKkw?$}vI9:ؘG-^kZ'm!P%BpD6G k,k4"[I7;le<ٖ5*pk5/~#,~XBc$ `|]/ƽx~ɴ1p.,4nyi 0c:t.ͫ:)>vo|	IM^aeɧO l37:ZFv[He1@*w994 C<au`gL;UUL(aW~(n$ 38%jO.t	ʋm4'<??e	h:G4IU4P<Yna\?ֿk۝F͒[Sed2d+Z2纐kkv"0<yeE;fĻ&s40=41 CU=^=lK[kk?t|[^U$}GF=[_|AMCI.XzZC@ # |;uϏ:~7|7&&.#1H`GuA>? %GC.|aR|/0ʖq3DS,[ԼlHFyHԧJ.Uz"?hLy
/Z^[HѬm0Hvl4<p#6x[
*Oc][\4Ndp1]=x g]Y-MY&Ld27F>u*Y`烑
~Ͷ>$M;[{=>ȭaח:؜?+;)ahՓ{z6_~"Pg<ZjvK)es;^[y(f%FzG\խuk;ӣX.E{|q<)FNFH+8~]|T[u_xLmNXm9glz{ƿætoX	'5w#׺J%zB凜]=:t:G39d
#9R;mXMӾ\]~MC55ͻ\Fa݁ 9 s_N <}z9D(+i&SӢ5.#̸(:8<?|y~ỏ Bwf]яXk
jhy8xWSY(߳匋 YVOR>WC#.]͏e\_O?^o.m]*m]h{W%]P+};V5]Jiar%F "1~BrO??ϯk_MM-WsG䴊BLdLw0W#
~ l}/OvyyC i$D
G]dc8 OMM#u#ּu}Vm	&yeY#M O"O0ނU{$|{7ai?v{}:>$ibu;XTqfzU=
?I\ S惨\.}w6:nL?tK&3תq ?<M64;C+ g.MBFLF	q\ 7xx}|;iw|-i+$Pp2'e3=kE)嵩> xV};{;[$5wK7z#0ʱX޻=++
ߣxVC5ozѻMcoyW̙!eQ ltM}u<>,zi[v6$-Ic2#`DI/k\ -~fS5xo/'
	a`!@2atgii gsqax|m,]#0xT$!r9.°&y
K61 "2D)y"{Ϫ]N;o%fN%@l$5F>k[c`9=ɯ枧SQ{k
|EM>QPH[H%91&[_?tY7X\ kc\Z|-M<ih;¯mj{	KخAfQ+2qZON DA6f08}Kl~о7~7n,|HxCe+v& Wňae[[6Tn渝b)Ted21s*]h޹7gK2B(d71WNPN~٥;>%h𵦷}wMmK˅g)5Og6$m<Q"1X(#<'ouY[>)%!ԮEb#z<>6淮MelmQ)(TN 89V*oC-owc۬Z֛JT>ֽOF,4;.$$l`u,a^M\,մjHF-Xڇ
E{GחX<UuIdQYlGX :g?X;ծtozO}YNnV%_ݰx/*ކ 욞;۹enl jqcIuHlwm_Xgx}J0OS͵hc+e,vNJ4~ʉnY-{^/P-fI)"]6hC95,U
|?--_Olmt{MHom 8յ\ -VM"ԢWh GZ_}¾|q.e`t[i)ȼ*`d!c8-#v9wL{2%ܭw~7Ӭ|Szm:ζI;iƠ_.7$覵$>u[P7n,CKax7?ZELq
P'efyc'q+?iIm~~#=oĊ5ZT`_mcc8`zk<4.^Hƞ2?t/KmBxcgm`
!s^mwo4yk!ݬ6Ɲ;nw!w'hվ2|Su\ĐNZζml` czqX4;{[x᷎]8*F:vgS*u6&'6? K]K_.IyFmn ͤ0Xg,	F?ẵ-hn,35
U/Y@q@W'UO0M#ټ#?Ihn >Xԃv5)-'TKYeB0
NF85f١1f*~{W'7 e 	u9HmoٰKp5g͡ύgmo潖k{bmVU0ʤ8ʒ
y9~w E5ŷM2\xŚBɾiz1zgGn.</}^8]ot*Qsp¶ſIIy2ӊ_vP${uwyqP%ݏ@&Ŀ-xN|u{J혃=@Q^ab>#|FҴ2Q#X5Sc]*D~~N@ ~"-|a?NmZ{ۍ)s%qB?yR͹ye|SFs0ltaHW3d{-ךw+OJ4뫝cᯈ.nnciI$FFIfezw
J\r<,{,
:ԼѲn!v5?_ݏ`fnfm4Y?th?5|*W'_
-:UX\oX#,6s~f6|+fk:tkxEE
	XG Y?zq-# +~ҟOD5'Zд-B=Z*l;A20jυĖJ9gxۯǺVռ7Nho S!Iff8p?c >);-n]w¾(tьuPá8fj8	i>Z4=Ʈ|cFKviM} <|Xצc?fI|FǇV:\7S40lHJq0Z
a
L?n#+@UN#	tJPV'=^vڵ]cHtmnxf](e#jO4hN |C &|RQ]CEuFY#'ԤȊƿD h J㻍$n=F_+2ӈS~UjJ;ݵ^fXTdvg@3Chudr뼜=9y\}*·vkjIjbNhV6dH#uzgWUuuRա&Erԓ6RVA3߭F_Iߕ {a(Fo,^G}
fSi'm*f&H(ALW-97Jw_ ֛B _1[ic~nh[+7Vm6eѷҚif?JT\ 1<6)~Zs
ff練oBN)%GqH	ѾZ *0qOVȠ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (ݷ׆~џ<eTH?!n5pR_A,1ے=jeiN\)XvV䁞+Bm\XqhWj/&19lg)sK[T)ԁJ
SȨ| P#Q)Y)
ro*HWhaMe[v?l2qUĕWld
o4@$sV&} ؔ
$OU@yƹ9sŗ_nlYYv3rq[g7E$
sC+6ou37W+
Xx5fi[3_<iK],,Իzd4G	oYuiݦ,)gs!Mqk]>)"l1͸F޳詎%f|	_7uMK##d!%x_.0Hnkۼ
8sDhXH". TX S[F1Ivy?g/W?%s"8 jE[Tl0|5j.Vemtua)i?~'|</HWOO#?aW3	OPIubG.&Ԑ8~Qҿ^O.]áb^ aa4ԏ~1|=?MbK/q O}^ٿc]Zn}ҽ(VªCڴ:Nq,R6ct%hGRriݟN[
#Za}{*J,Hl3߿bE|Fx{I5*ûo'Tc'q OGiki/ojw F;࢚b7m2؎? kPiOc&ݤp~^"z唺d6 fHl(B>Q f (ԭ
su<vDE-P1 gFk
/1/Oe|+El,@!N?#^f9Mǥ^T[t~Ξ=O~~4REe2͓i/4RyيEeW!m;H q߄VҿIkcq#NdbA\']Yz?WWW|s?޼tqDD9xWLqg<jJĿYhD5Ƨ6Ҥ{59LmnkkJNU'b>Lkοb ڃ^|?~cLWÁH:=XGrIK4tOX"m/T_9 oy<qJQb([5Ë?TF?j񍠗W
GqnBgQWxN.u{+ωO?7^d/-ϕ<W[ks4jG$go'5.\tcZ4  [$Ē0/mBo5夒Q\)VT]HeF8szM xVOM5%{	Gw6qXkѺ&+إ~*xñk2~LpivQs>rp	=:w	5~񗊼s̊wu snOz6mHN$(K!9SGWmP-;z̯d[^.Bi2PΫI /pگ/w:=.([4yVay呎O[I p?^<GQs/3){o㯂J|)q>6.s}'˅UFS5?)]B_Ϋl-mYy-ߙݎ;.{W^|Ln$/:O90CT;0AʎE{*ƯPĚi  GlWr'O28UB*){8<oStafvM6b8H=~&i={P~/Gկ&Ihk~^.Mn6tTVh.:+s.֗RG,"T۾諈rGi0imSYN$c
}%>\hV[Ⱦ1n㬋%|?x*ivQNCĎ)퍣#'޾?~47Z-J(isvtʡg;esXQJ5-s;\~?\?xX𮱧4WB]SMWvD@|oQ~ִkS]^k;,KV+b#jG+A;K~7WaLپ鼤A*!B@"('-^ -wK/K}Z[rla#0Ff!T2.7y<W4wP^)8I߱"|^|E6 	xVD,̚ 'gZ*}큦dxumZ=[OiodeV`#n?Ykǃ<$s;xN[Vq,1sYOU?(?.i
cz5+MZf\K(^LpPdW,O;zZCѿ55X7imcmt\3q[ʑ3Ϲyu> h+ᾛn]7ϳ<c-=?=Z654k&1#G@J,׃lm.5}P,3f K6P2I޽Ζa_UW
Oȏ\ck#u][ڽ3?ʠ'RH skw'=3qhM}SQac~y7by<
i{t|R.jzF~[F 
rL@% S{N\/ǟ;ⅷX-BNmBfUv2|`<|$cx[#oF9oou=kAvnq>~5 I߇gNjwX%f7 c<gҨ`u~~ԼQ=[Z=;PԙX}"Ih$i
 I5JJQRU#hHρ|/u/Z,5+6zZʖS$4Q??k4g덥Qt 00wz<
u8}>s}p8 c5[Cr\=z8:qvUBPM![Xrc_<#|u?Z^ Hf) Dj,_
۪Aӭz_|^K\W;
oj<oS8 G/ڏT.5"4ƢDPP-h5KmkRYj^"++)Xt}MT;Q|m*CZ`qi1Q3TU8 '`~˟tV$>o۵iZ2Lg$ p XVJJ'-a4mS^&mx=+ABҨOj̬dV-h_.ú/<_y.ռ1RQȷ#I:Riˎ؝(`2zaE{=*~,x:dm2V3(Pj;9y XM#bMY%|*>xzeԚ?v<
q|'׾E֭YiՃq#e%~0kݾמ|}楩K;ƃ\Hni+ g}GR?ǆgH1Io\vv8RXoݐqN4'5ͷW[IKRXnFUBd ʹ=:F4k=ƫ+:N>q&ᇅeZKH˶Gxu<OlMzRo9.UR1nkcqBh\ϲ 1b*;ʼ7Pd]ɞkv{U8%x6;vנ|L[gXF8QbθXدJҼ*{D4wOM=)[I}|&@=#"Ӛ|;NxF;[Qm̪y23ʃ>mE }x
ƺih դ/>GR(u%N2foǊu[[
fi,,;RtoxCx-5n
2i塁kfe*6xע|-sggof~47|jʭvGG;u<"x/ jqZ6v+19S̊yfzWG9k>/t:-B[cm4$W@aU\89[!RÌ
V'O~'-<xUyD0eU~ia+jqak?n4fh\W,~+ԴI]uI,[k2: z= iyOƚ.]mu;s̈j֔aαcd8	@Ggx:(?>5 >0x!
cB/ w |1:0 3~ xJK^?`WYA9I#!XI+7,W\ix^,`ݨk߂Rƞs|<KcLS |
ޡ{451V/rI8Zda
kgB rN ' OjS#Ū+}z3^$?M%rdd'8lwTVgdv(ˡUܤLT"8XϭQ-Ii}*M4r[3ڠb7t!P^)5AZ^{
hn?ʧKcowBݟ7Z5FML6? byԟ jrqXpx+@$ 
Dd%}ƣ'&3?hFҁ _gM4%f
Tc$P2Y }i'}l$֐Jj@s@*-J[CJj'ԑrtC zb \SsNLTdER@*x4NRޤOHE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE5 ؠt +R5 C7Q9zz*;P7S@yC$RoȦ @.x8}@1f$_֣=EIb.9=i `S`THi 3e~͖ tKʯ2~Mt}G&2O$?iS*6F8 0
.ր/$Pd⣏n~qSۅQ/Wj/ E QH&c^=HxK/j ½sSμ#o@5 NA;^37ĉH+/(T>Z6=}wN-6 
 9¾O @[F9 뎬 [㷯}MBi%)rK[Uvѯ3 PE~|x^G tR9 ^=|ER<\]e _)k7h3
˹?WA?z ) tZOeVB[fߛ&zz%vsojvhTqyr)MVbq׌JSIhd׵FI#`f Aj>|wt9-܉VYM:;B6pLj0?WF%~'6"Y_o{y<?cogMRWP.&8	S$z})5-lGkr9>O5ݷQF8.G7b|+hEŏ>nlcr(;ϳgc4Ld|RMeԩ$32! >X
SXIw%爯<2d7Gvc\b[=\iCUoO`RMdQ`Tc8'$KlSP%ڼ[Gn_
l2r·*z=Oؿ0 FUa`~+ӕ~%qێ?}keOøXKIne^e\&⒓J=Q W|m i㤹#i1]*23#:=W2[})~ c9- s m[ B_.WZZd˞e`ÿjl- ?ڬRڛJ:4OjcdvQJHR!򯑸~r {Ŀ6~jcY;6n~uiLѦݔXQdn SUOd'OKG
#wځVxMgT<IXYs([H#n@ g H 2 cޠ=6K"?_1~(<؉9EƊ>+{5i~y_9ܿf&Ո'ҽ_X궅>pkiP wmq~<3~Uqj i־%6ka.^8fH˴0aֳ8j^+S ϱI xMCC;kx/Xqc0Ur\5\g	c#ъ|?wG-R>@j_Z-uDd;+dd*GGp3>@1G͍ĚjkV]D
Ym̭ݲv-y2=꧙F6UaGgd h5ic1|1/@ԣ pxaȟSV4pƯ8L AWA-m{BZ
J@ǧI<)|oxAx^$.!oebR2sX Ƀ:NϮR9i'_MWu夓jaj?c+} i*7#PQ~ɟ$dӾ-'gV5KXu5g*(6yM&Ќ]Fр:Rlct(tm1Lp-Ea^<vanN5sWZ8]. W3ƤFy9CeEݽoLrO4q76Zt
@#,)"#|@UG Wj fyAǭs|~}mD24+6~PYGAй|I
1'Ҷ>0_ q!" EUo>t=AyrFy1<x5~>3o:fck!iR%Q2\L'DUJI,O-ah2GouOYm_:_F}GA޶s l7Yc\b<|c˼7uv~o7wγC]o>ܢQ}rNo'nU>\@de=+c?'j齏][jys$TOZ#ts𮗶5ˁw^.[?v;u.]ջt~]W4#n&>kS<x<դ~3"eʗMI2 ӾM-vu"ty_&F~}+5WF{{}7Y÷IJ16Xg8?.pH#<ǟ>FPhT tTi 04?:v]++CSE|^ϩsjŠ_@֐ AһOu<yaAmiu-jXT2\
+Cuizfÿ
Wh9Y.6{1ݯc$,1''}&У%uGRoşRM'ؖ
umb-eqc󏸯~(x[}gU>$VA,H@;Tʿ*R?[X}W[0QCУM{R4&zO+=xX#e3P_%tu Eqs\?~xI{^x'ӦeE]+o r56:<ҪƊYT5 d `#mZ1-4{Fpy+d&6}\+ׯrisY|ѹ
Rȸ6]ltXtlQ=|'r۴=?VdֿV^VJm+L y SOBEOe|#|y~?od⺏Zl</Fmpx~B7y#8QI 2 BЏ%>4~`M+(t[DQX港?z/Is{k57|-7rgҽDՑm=O/:_xF^mU>+o>VMh]zg\xKі 5|$\}5O,P F~\ߊRѓ
~P`PzZ]%s&r3= bهD--Wry%%gNJx\%u/:}朎9 E{4j?E)J4SΤS3#B|j.-c7ZjWУ}1d?ʈɪOA&ZIUTW ?ʀ%擞 /T A6U1_ ʤ 0SEIT8"u0 PJ. 4u_CЌ 7kTAgq krO4; ܷZEı+oѺ' M'5##6_m4 P.(CLL )7qʿATjʶQ5l6*F, QvM J,Z[\uZhM&h񩡨zj)Hq&ACpTBR\&iP4\P-E)4)hJi]
й◥( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (8Q[4 (FlP ZnA'lQNC=@SOJ v=)}.f>:SKqC<C>:n9G@Q9?r~ ySS~0ӻ֤_~_nfUfA  
$oU^qTӛ/L	ׁL+R* @WԱ2|i0hdNJuHތםT|~$Я-fR+ pH+JV'R:((6Ъz@ۛ9ie&=3Z,ﱯeś{?oJ?i([c].:zyǊw~4[08"=m{un}~|,dc_j25=MnXCj*`2:g5~&{x{ Lx_m4'J~_>&]@is C(73a_h~ ?`UoY0߄g%w0֭MG QWw.C<Wΰ'J
@%= ibd0kYb,͚c$]
Iu2 ڟu
K)\Gǅ쇪kѫ<Y;
-S>9
l13ߥ|}4|GdmGG*YXOG\r+kp'#_>Y5$nq>U ^65ǿy=Dhמѵm+fO	?0\ օho)c?- zO-QA?Ҿbִ]Cʏ M\y4vVթEOۧY v ak OѯQcbI 
(YQ|$ ֒B9]}Ni_e~ɵt(q/x =!@=/5'b4>
 /ıflUY[1|-|@wUt\H t
PfSY@߶zr vU/|F Z2\L#eo7O9WO_o_:ҒbyiSid?eg}GoxIڬZU#U	b	? ^б6'-{F -C7[7WMHNgz#o8{=at{~$rπ7ݍ@'9?
|Z=jʗj0aӌ
Gת5#8چ
ctt1ԙI*: (do'U9QC)#z7o
^x$Go侟+*`ǃ7J>
[Ǉ-OHs=	MqԓRʧϕG ~ 
]k:ׇ捼D|2t
J LcmżM5kS)|/u&?٥ u]o3;ʀv~8xOYpƷ	GzMwq׀$J7Ki6?)oݭSִeQI(y9ӓ{}#Qh3kݥi!:т
#^o 6'h:=Ω}mʷ3%4c@eTHdǏ7fмUcˉ KiZxae  rT}>v}-6:oqi\7-I,*2*:p*JSMv_#TZ1oٷ|4hU7"	00W}="LπPuݭ]D^vlP]_⿁wjk>&	s^qZp>A3Gl#M⩤Η1Gp"[OR|0xz~(僪5rO~1~ЖS<e)>f \H ys&Cc^&8|pPaO2Azz7;_7
 f$+E{bUIPH?θqs
J*F$>eU^<u(`|CNYnActZMv Ġ3r7k5S6'ssf+K Ǡz<}ipƩ?Cdx"imwX]2J [74o	ӎ!s|f}ߊo_4=SP&cݐkվݿ|9$kE#Yf<,ż$
lm^K-QOד5xs?7mėK}#N
Y S㇎?h_kw:v&}13&¹p7gt#QEFr Mu~*_|:6>ez)O_
}Axj8~kZ]ԗŤW,xʫ|09q^vcU`iNх`zh_Lk>->-ږ2n>;`)Hc2m A5_౫i~fg	_E32'kP\'hctJk!_Bӏzo=-	X%b"*S9tEe\~я7W^!A~3 >4Zֵˋ[+V(d܆r HvڏGgwW.6onkyDBG2m*AVa*in}e \	stJ_xCg4Ϧd"Muk	3uˤ:x:;_{
UJFgCJU-mIU>%%["nXW~?^$xO
^8[Oss |;/>3ZLZ8a|{hR+*T'3?M$|ak	Ǩai)9R>xftm'J&o2Y8h<[od݀Iֽ=fba^H{[ %)q(nm1R$p	}G]y(@1?&R֢69
gxћ󚫲M(mm
 Q\;[V;T^$gFZb]ܟTUZ-W"MX?_G	kgK;T0rdӐMm[+*kRTSm 3RY&_ UvIXEUڲl55pHHS>wTڀ_T&,,QKj܏%?ʛ} A\ǈi,w-̣oL#_GQir2Yڱok?o Fڿh? ]c {ԅ0*]SWn+3@oآgZ :Vm5?*)doݷңf(})/J +}
ʿAZ\htp=ZV[
j4;~@HjU}jJI!8mRPJ )
K*$sA\RJV%8ԕM*iÁK`
r(ɧҊ(((((((((((((((((((((((((((((((((((((((((J@sESJQE>P
(?Z+W@Q7ݩj75 GJ4'ZԌ2)h=*@E9MHE uю(@GR(曷槧ަDji9nފ1RH_~\_RU  -UqPST
,~؎f?O+H)s@;<O_Ɣr) V̙5mBFSB]J
"_9eTfHܥW8=k(JI=q(}'3x^nH8 _:kc'uւR0m!
}MҾVtL|Ϝ{!5Zpq;i*J-3|4.dny4 yɯEjj:}̋1y ӡCa*$yWK ;赯-~sn|zd~QpEL(89^^}7 u#_ծ͖=[{"=Kz_jE3FsȻFS'=1?௳\GI6q,i@} 8?3`{׀Btu.>fzXeq9kRգIGcE杯Jym;\?-?Vcݷz.~A_?ߩrW}kZu/6oi&4!
\wٺ
uobs")	 b
o!an=`lԏƺK4vO8 s.9FEsV(PHecw:-gT<-nZ8aI<kмsu$4:[w?3rOkL#[35sޑhlk/\d(qסRNyICsp-<k2mc>s+o୤km=W+c8 `W %kBRu
NX[[!Uw5,I,ztͮ 1B^2W1s|~s3	^N#%V<xoXK9Lgӕ+|-|E dXu;|9>"Pc%=jsYThg_/MZm#Wl(n3-.+ɉ +/_O?Hgƶ:^7M+RqNOlkg[6 ʟ|J>1Yl$|55NRj&57o#>+[^K[۝).аhC#qGe3Gz|ԟ㟅Ach>L,;du`[ǃ=7g쥨cUmJFCjEq/dc7Q_{~οqWnu':zD	l~O9Ui>Z?G4~]OK~۽ͿV><nHs0 	@a{kxYʧ!ZZ(\4_aωthҶzU.^68$w?i |w>%xoÚ<((#w<79ɪþJ]yWzy>'Hn*-ɕPnW-ིPI1VGɴ>r3q^c.7=՜
#L-
mg{A_bqgkkg{<v>3l@f=8WSC8ЪŎ	5kºEn?nW>`l1
Lᦜo>H[Ώ0yAjG?v
'4KH/GdB;ypF0ך.m0B̯,OJ+bM(+8ԼW&g2,
?&v蟰4KkC&x=|SCe8R:_mFd-9DW} #R|RtfjXYp\$ɹ
y/CӖ5lB?bm#vסh7אxMyPMϷ
ê Ƿ|< i M=cI$ߋ{^{]MVYP(@d돘6r>a 4i-	-Lq1'!]WNb e
_$VL
PHYp2׭tSߡ[|C;w|vjxHh1bn6I%8|U>2|E*xGZ{K(b! ,,N cԻ2+tUpqUYheYX=*ucOkυZ&n&b qhOi#eee$g(?ƾ 7I{khV|UzZj?|<7=
?
̖ׅ흮q d/?Qׅ^={zrS$?kGq hwW*,
VG]ۀIZ?~M$WyKeWןH![^.\=YkR<p9 fx[wo
swL
s	ֿV73
"W{i8oZKxT`JڳίZ#uKx~G؏ZG Nku}?~]DtlxHT0 ~4e*eG9UFb'M''럳mCzFOBpG#H3UZ/,>"[o)5yn%0`L
.o~?:eXoNqKJ塂'ϻ;1Gdb8k&3}9EV?cx0))+s
nyeVʹ7ǼeO[ ,bՑX꺫-7\{)jwuZ/n7'saQ~Yu=RsԎ\!Tpxu}ޑ&Zw#-?{׿>`O|wojG]TkZ%i^kOUsNK5au|ATzZ!n *ղzQ7?:G%BC\垡Su7=z\4Z1=#oɍ~S64 *.sm4| .~ 	-x>O\W7Oƴm2+6LӖ\yv?ID?J/қ$ !U?kQ#d7U
$ #}
,|DV5qzV}qejdR	+Q\KVl,27ԈsU;~f6HɢRTQ Z  ո*%[*%N=)Ҝy[N<S|h_K@92i b((((((((((((((((((((((((((((((((((((((((((1%Iъ b4)S)J˶5E
0()PB)SJE 1J8TQ_)*LR2S'Zm::P_ʦ*7_PT0*5(1RތRUv߅Z~@G[Sm~5 U~s7RJ?IĿ ~
Ҩ B}r
|\Pөaih:NWPEG0~}9Oq.YW[ɍHm
Q(ݧ֝NT]XyrpX]tz~U ?7z]a m+FydoE~ٟ{c5eJ-޼[&%ֿquI#h#M'OjDۗsU)3 ſ,vШO^7_b¨  y:[[H0UU$];sh| 9yfmQ E	VZ[7d ?)oluح.&7Cg})>Eoe#n%49PC8Ri\ꦢi; ɧ/#">E}A^}j4sF
0`IF׆E' AӃWsޏv! 
z횆oO	k?t ^^>?(W
h }~:6ߧ_Hk1s2ۆI_EoX+	!o5#kޣ#mvjkSZ ǴRWx'Pl.w}K<{ijkk8./nncd_1A=@bdW=Jpr:)Ԝ?h	*U.z^7?VL.瑿v'򯤾 _X^x#xX6+!y,"VpKg9γ7>EiGUm!E.Y6
yyGVQGnde*A
oj:&izJ)nXA
l%Ċ7`X&ZDa"X'W]:pjJM#u-/Byl5+I7Wn<֯| j:Kt&s$7e$vpMr>{4{sֻ_>3n S: tK&1;wn¿I }Co0OKw2ioa__uw·45yB?~U~Ǻ?:֌) /_a<;!NJ?!i^gU\ Wj:as_?Q%^v]],7pm{UU S<oOgR6]*]0xduB(waTl !%7֞eFz<
͹[npp3OZe/WvwVdE\0zkQ9}z{Z^_j!m 7(J,- i(} gWp!VJyWp;Gҽ
aτ^$[W \bW	A^h{G~~Lخl2MrԒ"]}#O6/ȣ8,v@m^hZ߯^;$۾AFirDk0Ah1ݞE~t+Wĳnsvi;gO
}
XM3_׍1ev4nGemAxgMwJ	~ͦv?k+W;៘q Z `;Ag -{ 5e[+}~mA.k>jDvqzub<93j91P"n{Vl!Ճ"oδ'~/g񎊡Mp:_}S`dI͜-yNB1~q/zJZr3ڭ|W߭G⽰W|SBZMR$\g>1x|߭D|d[}ɮq5<?ή|^-Qo'sUbW?zq ަLSӭUަwza2xtmt1VG) _̓\*kMc1%12ؚ8L:Ɲ:	VUOV;տy'FCe k*hvcִs'W
i Zp_	Tw:-RjK=rVz7|ݗ
mw(7cUI6/'k_ڗ#G?E[P+Գi"'^ J@u?
i[GCZSR
^qֹ3Z[;|PU).LK">Q[i_EgVMk/ʿ9@ڴ&+^kB9:
KM֡Yy#J	rWWn+*_h٩Hi8ꑎP6jo
ZeDӪ8O#*
#=j:uQxZ>JiHQE( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( (<(iք^`7>ZE)iN
>>( :SdGJrt*(REc4 ^iȽ9W 2*kɩ)P 41Eƫ2 J$|jO߅N?1F$*GQ̟ XFE63NӕsN
()?ݨy>J ( ( 
2*.qOuhƀG3-@[w_gܿ1 U|7¿ SĚN&%j貲}+	BY2D[yG)&
[/M5zGhRYq&y#
b#
^GKh}C_hOSAy7KQE 
Ɓi#K5
3mḩtm $ɌW߷c**X ?zGE#E\mGO[
tQN4W&WI{6 l!I6-Qpy_p?Z?
5ωã]yJB; # z/}\+GM?McIti8d
JnuY8?0~22^gﯥYE+ByW]Oƕ]"-ƫWz$N?Y^S8Ni!
NE# Bm f@ 5[} F 
N7?sh#?ENmc t* 8 ʦP - ~k
`_5	0vFd? ^_gN?>.~;|-  _߉z,'8Y>616W׀]%.TYqz4O1NSQ[?
bꖋ,^_>+4?|^o
<h>}VG97DⰣ(4~)]C[  ,<! <'_Z&ʬ~_j=)wN [WW	FǶ?V|
u߿0_KW  nn? 7UnUWFn;Hm0Z3F$Y#?χ~#k$vF5ヂz~bkuxP" U6My6o
o{\1oRFO5e%I]MTvG⟄o0ſ.0?uwY_Ǎ[M7=Sǂ/sdk??Fx'X.5}jfi`V%#&@6zǧ?OBEkB8++ԊVuWR|W -/;]G/,pcʟgK`vp M?O_>,7<E.i5?T+cءP#i[XD)U<5knX~]t8eRe6$teNIM|٤+|>)6j#~"0rxq_|E?y_*NHDW_Z_$|'o(>_Ypcw`+Ɵmg/&$&|͗`kf?ྜྷ5q_Mr]]ܕ_0UHׄAX@$?ҴCm\ivU̴=[g
>ա|@3zǨl# H.rMO<Smb_ּFq 1mc^m⏍]n#sKewdhA9)ϵy^a5yv?ddO}jX9#4JF޺|nms?SxNqκuO	X>nO"e#ƪ\|rS^G}&Vǧȳ؞樛-|\GOFkKc|i(Z\Ǩ/Rm_kĘCR G_\̎Tz4>(Pԇ;pQx07njힿ*;u]mA 9gy|nЃ[~9?iZQ%ŝH5Ran *[q[֚0R'-5bݗ
MPm	z'TjFM>bZ:kS_+mSmu-=hZisuW "B k/ܠVƠ<NnOkJTbkM@em/Bzmu!lZ!1V|wyVT5
 a[SO_G>n#n{S0 ߴ?XVW֔3T&!zL zO5 ^֥V4Zҵ2)HTتIHRQ0o۷5@?ը h٨bz~mOm T*uSQE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE 5ІHj _STr/
֎\Ҫ֜NZp((BRIҚMH"t(c5%F~FMIMN ( lU5ZTdTQp2r
 FjlITj((	QRPHQA8EP֣Tt Tң!R1hTRS:
e^|,(
m<k7٧~qqmZ$eR$~Ú?\ZE#,-488jaڿH.-#B2\ >~&ޟo#DHo1ӵyxꤠ=L6aȭ4~j~~ 9m H>.4>3ZoA ~1\L 8#?ָ	3]*x[	LE( hw0+r9]%S 64	n4?H7q%#pc7_.n/5'Aa[۠Hc0=+ңDWw'4ݐ_۝Z_;hs6>  vji+_jJO2322$?OiRG;۸F_J__i_ !u
~ΌXUd `|g} 9[MZh6Zwu|>5ozB޽_
97zt6
ǭ_NPi6q ?OMhvWx^Ehhsk፤e
5ݜwr.jΤ9iF$ԏ_
uw㧂Z^iqw-IizFj <_:W&dDszt6̑ E'9|'J5Z\Od|H3ڇ-5KSQTkл"]Td|P~ú XHb78"hj6ʹo4Mkopǹ~YlVmyt*e$d~	|B&ҵ[[Ė̱HZ g+ikkK=b[$# u #MմZĺTuo<e2\`6O^\^qjOBMkc/;/%${kG1Ҿ<OOXa]bۚ4!x _mhzjvB5S?zJǓT\	zG-k=D͚ H%B[
XP%5 E9_+Uwb׵CE;ſ^7mY<k."^Xjs1586#|[ke~^eA޵~/[qw<Ҽ-3W$/.yuu36wb ҹ=o5J#+>nԣc_Zƹ־\+ 㵃fhү4xLoSL:U_	fZ2~>nJc
?.{E]eY{,oݚfg*v<kQ$gcצ^-loJuJlɍ4qZ}4hs[Iᆋi/jnO3zM'xmUdҤXW֩V'٢!2i2 ^HOJ
.En!{6k-{ma ltH4QkOj%MRP>d}~5e~s\6^>֕*>Z>͝V`߳k)Zan{T3Y[{ʟ>[mk'&ARGYm/U{!qZT}jZyCR'uFAԏ=rؗ) ?^{ӶvZq2kk֨V;Mc~nⷬuml<t^#ܿ_rZӲ (mM_-&n7-s6[vR|4^LԊSبrmeօ~~\R*&R*IS*`TXɘիw|~۾ |5SIHhzu->Jj$*
rQEHQ@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@Q@f@&:m=PLS"nM+
FW@
(s.H
'Zm*H)iPݥi QE SS#4   QE 
VcUMTh,GxOo­DY 
y^A$IQ֤C\iM!LV kFE!Ȥ is3@SYsN" EQ@Q@Q@ʹel\*J( U
8( ( ( ( ( )7
G574)|VW/_67Hw_*[)"ڿkH}Vl1hvLw)
S3p*2sNwg`)JZ}Jͺ(C
sAKHS+p)T"m
s ZeMcR⺍33Q*Ϻ{o" _ʻ"4U 
f KVN|*քTtbU?g%S fd_+W`"ͤFXdj2>O!~V\ r3rFI"ĳ仟"5ȇQ~11G?¾<N>T}l/bۧޡ57G=VQʿX|$O.d|}'YSDԏʾ¸=56ȯkHV>{ёStx+{߄QsV| X/x80CZD?*>ՏʈNIJCQ?vT/~/ҶRh˕3%WC`vZ	c{ƣ̿V2\O-u$'ץIT 9?w'ix=
uVW'j|
`=UQJY3Z҂FۯJշ*/zzU*h*eGcz5e1/I'NCZFsw%SKm|֭
 #MnT!Klu:E ׳V<`qZso~+^(AXv֌xk_Oksj-(~bLĿULJ/~zs[mšDީժ
jm X_\2V->jE#zUqYRnQWTԲ	o'
ORU|lUȟ4mNE9EEJRZzSDR-QH(((((((((((((((((((((((((((((((((((((((((H˚ b
&L 4
(nlQG0) R?ݥhQJu3qN 6S )@
ON
( ( ( ( (9W&0ժ1@Vך8ԔP FEC'ީ9 5:Tu0@ƽ6DtLӂ k.i%4!'Jy4l<Rl4CQE QE QA8 ٥@0( R3bNh_Y)٨ ,N+)fCMj}uV\Y-0f4K
Ml-GRӳTH<lu-
JQ+aԔ<K{7&~MaRPih ( ( #4Ҕ(=SbhAc[fe Q6ԟc\Ӗ,,B4((ZOs%?Pˢ 
ny6SʇvsGXe õwh
C5}i:h|K 7B~v1OJJ;T{"<o(v}?*Eoه<nO* ^C5xi!Sw L Jyd;Xx:6vfO q  
vn~&Pk?9;Zcl/oJF/hxk|< WTo ]{
_^oS~r1)
?v/ٻ}+W
~^õ1<{JM{{bx?^sY~_Ң +W'c̭#kB8juݪR!C5nE!W+|h~ZڴR3q9hsRå-~^º_MM$kjd򘖺yF̀tYKS)WO1wi9c1l֥"6I_֜8nbK.h/Uqa!io#nJhCԀnnMPk@!LՄbT ) QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE QE Sd\Ө?PEPEPEPEPEPEPEPEPEPEPLfE 24>( ( ( ( ( ( ( ( ( oKE GRQ( (wSJO#+MeMF3@QSZPW1	82|#"T%0 >FJ@i6ԛ;X.2E.($ޕ>FA\gգy+SC
w`SI-V_KV+Gr1WMY(_J9CPr1_e*ǔ(r OQS\GGS`\EJ#O4mW!M	X&@\;URm1Uܪb1{UZVbO$U%hV(s|y+Gr1Ge{y"P(}iH$Q9C6*{S[MSڴG(c%qJu/Ҷۊ9CF\}qҺj
!r1
G d}BQI}h>QCҏ:Qas}ڍt_|6  
"ݪNm#]'Vb@VM'&])AJ4;S dкVJ`3S
,6
ڷ`4s5S%kXibO)
Zm^[UZp@K9Hbju9b(((((((((((((((((((((((
```

## example/example01.ipynb

```
{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "# Cohere API\u306eClassify\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u3068\u306f"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Classify\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u306f\u3001\u30c6\u30ad\u30b9\u30c8\u3092\u4e8b\u524d\u306b\u5b9a\u7fa9\u3055\u308c\u305f\u30af\u30e9\u30b9\uff08\u30ab\u30c6\u30b4\u30ea\uff09\u306b\u5206\u985e\u3059\u308b\u305f\u3081\u306e\u6a5f\u80fd\u3067\u3059\u3002\u3044\u304f\u3064\u304b\u306e\u4f8b\u3092\u4f7f\u3063\u3066\u3001\u751f\u6210\u30e2\u30c7\u30eb\u304b\u3089\u30af\u30e9\u30b9\u5206\u985e\u5668\u3092\u4f5c\u6210\u3057\u307e\u3059\u3002\u5185\u90e8\u7684\u306b\u306f\u3001few-shot\u5206\u985e\u30d7\u30ed\u30f3\u30d7\u30c8\u3092\u69cb\u7bc9\u3057\u3001\u305d\u308c\u3092\u4f7f\u3063\u3066\u5165\u529b\u30c6\u30ad\u30b9\u30c8\u3092\u5206\u985e\u3057\u307e\u3059\u3002"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Classify\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u306e\u4f7f\u7528\u4f8b"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\u9867\u5ba2\u30b5\u30dd\u30fc\u30c8\u30c1\u30b1\u30c3\u30c8\u306e\u5206\u985e\u306b\u4f7f\u3048\u307e\u3059\u3002\u4f8b\u3048\u3070\u3001\u4fdd\u967a\u4f1a\u793e\u306b\u5c4a\u304f\u9867\u5ba2\u30e1\u30fc\u30eb\u3092\u4ee5\u4e0b\u306e4\u3064\u306e\u30bf\u30a4\u30d7\u306b\u81ea\u52d5\u5206\u985e\u3067\u304d\u307e\u3059\u3002",
        "",
        "- \u4fdd\u967a\u8a3c\u5238\u306e\u8a73\u7d30\u3092\u63a2\u3059",
        "- \u30a2\u30ab\u30a6\u30f3\u30c8\u8a2d\u5b9a\u306e\u5909\u66f4",
        "- \u4fdd\u967a\u91d1\u8acb\u6c42\u3068\u72b6\u6cc1\u78ba\u8a8d",
        "- \u4fdd\u967a\u306e\u89e3\u7d04",
        "",
        "\u3053\u308c\u306b\u3088\u308a\u3001\u30b5\u30dd\u30fc\u30c8\u30c1\u30fc\u30e0\u306f\u624b\u52d5\u3067\u60c5\u5831\u3092\u5206\u6790\u3057\u3066\u30eb\u30fc\u30c6\u30a3\u30f3\u30b0\u3059\u308b\u624b\u9593\u3092\u7701\u3051\u307e\u3059\u3002"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Classify\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u306e\u4f7f\u3044\u65b9"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### 1. Cohere SDK\u306e\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\u307e\u305a\u3001Cohere SDK\u3092\u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u3057\u307e\u3059\u3002",
        "",
        "```bash",
        "pip install cohere",
        "```"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### 2. Cohere client\u306e\u8a2d\u5b9a"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\u6b21\u306b\u3001Cohere client\u3092\u8a2d\u5b9a\u3057\u307e\u3059\u3002"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "import cohere",
        "co = cohere.Client(api_key)"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### 3. \u5b66\u7fd2\u7528\u306e\u4f8b\u306e\u8ffd\u52a0"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\u5b66\u7fd2\u7528\u306e\u4f8b\u3092\u8ffd\u52a0\u3057\u307e\u3059\u3002\u5404\u4f8b\u306f\u30c6\u30ad\u30b9\u30c8\u3068\u305d\u308c\u306b\u5bfe\u5fdc\u3059\u308b\u30e9\u30d9\u30eb\uff08\u30af\u30e9\u30b9\uff09\u3067\u69cb\u6210\u3055\u308c\u307e\u3059\u3002\u5404\u30af\u30e9\u30b9\u306b\u6700\u4f4e2\u3064\u306e\u4f8b\u304c\u5fc5\u8981\u3067\u3059\u3002"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "from cohere.responses.classify import Example",
        "",
        "examples=[",
        "  Example(\"\u4fdd\u967a\u8a3c\u5238\u306f\u3069\u3053\u3067\u898b\u3064\u3051\u3089\u308c\u307e\u3059\u304b\uff1f\", \"\u4fdd\u967a\u8a3c\u5238\u306e\u8a73\u7d30\u3092\u63a2\u3059\"),",
        "  Example(\"\u4fdd\u967a\u8a3c\u5238\u306e\u30b3\u30d4\u30fc\u3092\u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u3059\u308b\u65b9\u6cd5\u306f\uff1f\", \"\u4fdd\u967a\u8a3c\u5238\u306e\u8a73\u7d30\u3092\u63a2\u3059\"),",
        "  ...",
        "]"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### 4. \u5206\u985e\u5bfe\u8c61\u30c6\u30ad\u30b9\u30c8\u306e\u8ffd\u52a0"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "\u5206\u985e\u3057\u305f\u3044\u30c6\u30ad\u30b9\u30c8\u3092\u5165\u529b\u3068\u3057\u3066\u8ffd\u52a0\u3057\u307e\u3059\u3002"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "inputs=[\"\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u5909\u66f4\u3057\u305f\u3044\u306e\u3067\u3059\u304c\",",
        "        \"\u79c1\u306e\u4fdd\u967a\u3067\u51e6\u65b9\u85ac\u306f\u30ab\u30d0\u30fc\u3055\u308c\u3066\u3044\u307e\u3059\u304b\uff1f\"",
        "        ]"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "### 5. Classify\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u306e\u547c\u3073\u51fa\u3057"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Classify\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u3092\u547c\u3073\u51fa\u3057\u3066\u5206\u985e\u3057\u307e\u3059\u3002\u30e2\u30c7\u30eb\u306e\u30bf\u30a4\u30d7\u3092\u6307\u5b9a\u3057\u307e\u3059\uff08\u30c7\u30d5\u30a9\u30eb\u30c8\u306flarge\uff09\u3002"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": [
        "response = co.classify(",
        "    model='large',",
        "    inputs=inputs,",
        "    examples=examples)",
        "",
        "print(response.classifications)"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## \u30ec\u30b9\u30dd\u30f3\u30b9\u306e\u4f8b"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "```json",
        "{",
        "  \"results\": [",
        "    {",
        "      \"text\": \"\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u5909\u66f4\u3057\u305f\u3044\u306e\u3067\u3059\u304c\",",
        "      \"prediction\": \"\u30a2\u30ab\u30a6\u30f3\u30c8\u8a2d\u5b9a\u306e\u5909\u66f4\",",
        "      \"confidence\": 0.82,",
        "      ...",
        "    },",
        "    {",
        "      \"text\":  \"\u79c1\u306e\u4fdd\u967a\u3067\u51e6\u65b9\u85ac\u306f\u30ab\u30d0\u30fc\u3055\u308c\u3066\u3044\u307e\u3059\u304b\uff1f\",",
        "      \"prediction\": \"\u4fdd\u967a\u8a3c\u5238\u306e\u8a73\u7d30\u3092\u63a2\u3059\",",
        "      \"confidence\": 0.75,",
        "      ...",
        "    }",
        "  ]",
        "}",
        "```",
        "",
        "\u4ee5\u4e0a\u304c\u3001Cohere API\u306eClassify\u30a8\u30f3\u30c9\u30dd\u30a4\u30f3\u30c8\u306e\u6982\u8981\u3068\u57fa\u672c\u7684\u306a\u4f7f\u3044\u65b9\u3067\u3059\u3002\u30c6\u30ad\u30b9\u30c8\u5206\u985e\u30bf\u30b9\u30af\u3092\u624b\u8efd\u306b\u5b9f\u88c5\u3067\u304d\u308b\u4fbf\u5229\u306a\u6a5f\u80fd\u3068\u3044\u3048\u308b\u3067\u3057\u3087\u3046\u3002"
      ]
    }
  ]
}
```

## example/example01.md

```markdown
# Cohere APIのClassifyエンドポイントとは

Classifyエンドポイントは、テキストを事前に定義されたクラス（カテゴリ）に分類するための機能です。いくつかの例を使って、生成モデルからクラス分類器を作成します。内部的には、few-shot分類プロンプトを構築し、それを使って入力テキストを分類します。

## Classifyエンドポイントの使用例

顧客サポートチケットの分類に使えます。例えば、保険会社に届く顧客メールを以下の4つのタイプに自動分類できます。

- 保険証券の詳細を探す
- アカウント設定の変更
- 保険金請求と状況確認
- 保険の解約

これにより、サポートチームは手動で情報を分析してルーティングする手間を省けます。

## Classifyエンドポイントの使い方

### 1. Cohere SDKのインストール

まず、Cohere SDKをインストールします。

	```bash
	pip install cohere
	```

### 2. Cohere clientの設定

次に、Cohere clientを設定します。

	```python
	import cohere
	co = cohere.Client(api_key)
	```

### 3. 学習用の例の追加

学習用の例を追加します。各例はテキストとそれに対応するラベル（クラス）で構成されます。各クラスに最低2つの例が必要です。

	```python
	from cohere.responses.classify import Example
	
	examples=[
	  Example("保険証券はどこで見つけられますか？", "保険証券の詳細を探す"),
	  Example("保険証券のコピーをダウンロードする方法は？", "保険証券の詳細を探す"),
	  ...
	]
	```

### 4. 分類対象テキストの追加

分類したいテキストを入力として追加します。

	```python
	inputs=["パスワードを変更したいのですが",
	        "私の保険で処方薬はカバーされていますか？"
	        ]
	```

### 5. Classifyエンドポイントの呼び出し

Classifyエンドポイントを呼び出して分類します。モデルのタイプを指定します（デフォルトはlarge）。

	```python
	response = co.classify(
	    model='large',
	    inputs=inputs,
	    examples=examples)
	
	print(response.classifications)
	```

## レスポンスの例

	```json
	{
	  "results": [
	    {
	      "text": "パスワードを変更したいのですが",
	      "prediction": "アカウント設定の変更",
	      "confidence": 0.82,
	      ...
	    },
	    {
	      "text":  "私の保険で処方薬はカバーされていますか？",
	      "prediction": "保険証券の詳細を探す",
	      "confidence": 0.75,
	      ...
	    }
	  ]
	}
	```

以上が、Cohere APIのClassifyエンドポイントの概要と基本的な使い方です。テキスト分類タスクを手軽に実装できる便利な機能といえるでしょう。
```

## script/activate-notebook-forge.bat

```
conda activate notebook-forge
```

## script/activate-notebook-forge.sh

```bash
#!/bin/bash
conda activate notebook-forge
```

