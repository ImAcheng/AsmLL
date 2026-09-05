# AsmLL
一個語法類似於8051組合語言的直譯器 (純實驗性用途)  
An 8051 assembly-like programming language interpreter (for experimental purposes).

由於只有模擬 8051組合語言 的語法 所以有些東西沒有非常嚴謹 (例如暫存器的使用方式)  
It only simulates the grammar, not very strict (e.g.: registers).

目前指令集尚未撰寫完畢 如果有些非常需要的指令 請開一個 Issue :D  
The instruction set isn't yet complete. Please open an issue if needed.

## 如何執行 How to start?
首先您需要透過此 README 最底下的指令集撰寫一份檔案 (廢話)  
Coding with the instructions below first (ofc).  

若您使用本專案的原代碼 (If you're using source code):
```
py __main__.py <your file>
```
若您使用已包裝的.exe檔案 (If you're using packed .exe file I provided in realese):
```
asmll.exe <your file>
```

## 小故事 Story
我會做出這個語言是因為我上實習課 (單晶片微處理機實習) 的時候，我們老師都用組合語言教，
然後我可能有點大病，想說不然自己來寫一個語法類似於組合語言的直譯器好了，因此我就寫出了這坨東西。  
呃，但有些人可能會理解到，這東西是個循環，為什麼呢，因為:
```
Assembly -> C -> Python -> AsmLL
```
如果哪天有神人用 AsmLL 再寫出C的話，記得叫我去看 :D  
(雖然技術上來說不可能 目前指令集不夠多)

## 前綴符號 Prefix Symbol
| Symbol | Explanation | Example | 
| :----: | ----------- | ------- |
| # | Represent a number. | #620412 |
| $ | Represent a string. | $SIVS ICS |
| ; | Comment. | ; Made by 彰師附工 資訊科 阿程 |

## N進制數字表示 To Represents Base-N Number
| Base | Symbol | Example |
| :----: | :---------: | ------- |
| base-10 | (No) | #15 |
| base-2 | B | #1111B |
| base-16 | H | #FH|

## 標籤 Lables
```
As every one knows, lable is a "mark" in assembly. We can call jump instructions to jump to the lable and execute instructions. But, uhh, yeah, due to some technical issues, please DO NOT put instruction in the same line after the lable (I will fix it in the future).
```
Example:
```
Lable:
    JMP Lable
```
(This will cause infinite loop.)

## 指令集 Instruction Set
| Instruction |   | Explanation |  
| ----------- | - | ------------------ |
| MOV [dest], [src] || To move value from src to dest. |
| OUT [src] || To print value from src. |
| NL || To make a new line. |
| READ [dest] || To read value and store to dest. |
| ADD [dest], [src] || To add dest's value by src's value. |
| SUB [dest], [src] || To substruct dest's value by src's value. |
| JMP [dest (lable)] || To go to the dest. | 
| PUSH [src (reg)] || To push a register's value into stack. |
| POP [dest] || To pop out from the stack to a register. |
| CALL [dest] || To push the original PC and jump to dest lable. |
| RET || To return to stored PC. |
| NOP [ms] || To delay ms (originally meaning: no operation). |
| BOUT [src (reg)] || To print a bitwise number. |
| ANL [dest (reg)] [src] || Bitwise AND. |
| ORL [dest (reg)] [src] || Bitwise OR. |
| DJNZ [register] [dest] || Decrement and jump if not zero |

(Instruction Set update datetime: `Sep. 5th, 2026`)