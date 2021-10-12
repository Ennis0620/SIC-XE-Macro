SIC-XE-Marco
===

# Introduction
模擬SIC/EX 聚集指令的展開
# Detail
### 讀檔:
1.存取Symbol、Instruction、Operand，不存註解行。

2.當遇到Instruction是Marco的時候記下前面的Symbol(Marco的名稱)。

### 處理Marco:
1.將Marco到MEND的部分從陣列存取的地方移出來

2.存下Marco後面的聚集參數(形式參數)

### 展開:
1.將去除所有Marco到MEND的陣列讀取一次

2.當讀取到Instruction是Marco的名稱時，存下operand的實際參數 

3.將實際參數帶入此Marco的聚集參數，並將後續進行替換

4.遇到MEND時代表該Marco結束，跳出並繼續下面的指令

5.若又遇到Instruction是Marco的名稱時重複2~4，便可以將所有程式展開完畢

# Demo
執行結果

![](https://i.imgur.com/4BcORCL.png)

# Requirement
    None
# Package
    └─Macro
        Macro.py      主程式
        MACRO.txt     輸入
        
# Problems
# Solve
