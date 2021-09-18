This is python code to simulate logic

# Running The program.

to run it:
```bash
python main.py
```
this will print a test log similair to this:

```txt
Testing 'And' part.
A |B |Q 
0 |0 |0 
0 |1 |0 
1 |0 |0 
1 |1 |1 

Testing 'Or' part.
A |B |Q 
0 |0 |0 
0 |1 |1 
1 |0 |1 
1 |1 |1 

Testing 'Not' part.
A |Q 
0 |1 
1 |0 

Testing 'Nand' part.
A |B |Q 
0 |0 |1 
0 |1 |1 
1 |0 |1 
1 |1 |0 

Testing 'Nor' part.
A |B |Q 
0 |0 |1 
0 |1 |0 
1 |0 |0 
1 |1 |0 

Testing 'Xor' part.
A |B |Q 
0 |0 |0 
0 |1 |1 
1 |0 |1 
1 |1 |0 

Testing 'Xnor' part.
A |B |Q 
0 |0 |1 
0 |1 |0 
1 |0 |0 
1 |1 |1 

Testing 'SRLatch' part.
Reset |Set   |Q     |Qn    
0     |0     |0     |1     
0     |1     |1     |0     
1     |0     |0     |1     
1     |1     |0     |0     

Testing 'GatedLatch' part.
Clk   |Reset |Set   |Q     |Qn    
0     |0     |0     |0     |1     
0     |0     |1     |0     |1     
0     |1     |0     |0     |1     
0     |1     |1     |0     |1     
1     |0     |0     |0     |1     
1     |0     |1     |1     |0     
1     |1     |0     |0     |1     
1     |1     |1     |0     |0     

Testing 'DataLatch' part.
Clk  |Data |Q    |Qn   
0    |0    |0    |1    
0    |1    |0    |1    
1    |0    |0    |1    
1    |1    |1    |0    

Testing 'HalfAdder' part.
A     |B     |Sum   |Carry 
0     |0     |0     |0     
0     |1     |1     |0     
1     |0     |1     |0     
1     |1     |0     |1     

Testing 'FullAdder' part.
Cin  |A    |B    |Sum  |Cout 
0    |0    |0    |0    |0    
0    |0    |1    |1    |0    
0    |1    |0    |1    |0    
0    |1    |1    |0    |1    
1    |0    |0    |1    |0    
1    |0    |1    |0    |1    
1    |1    |0    |0    |1    
1    |1    |1    |1    |1    

Testing 'FlipFlop' part.
Clk   |Reset |Set   |Q     |Qn    
0     |0     |0     |0     |1     
1     |0     |0     |0     |1     
0     |0     |0     |0     |1     
Clk   |Reset |Set   |Q     |Qn    
0     |0     |1     |0     |1     
1     |0     |1     |0     |1     
0     |0     |1     |1     |0     
Clk   |Reset |Set   |Q     |Qn    
0     |1     |0     |1     |0     
1     |1     |0     |1     |0     
0     |1     |0     |0     |1     
Clk   |Reset |Set   |Q     |Qn    
0     |1     |1     |0     |1     
1     |1     |1     |0     |1     
0     |1     |1     |0     |1     
Clk   |Reset |Set   |Q     |Qn    
0     |0     |0     |0     |1     
1     |0     |0     |0     |1     
0     |0     |0     |0     |1     
Clk   |Reset |Set   |Q     |Qn    
0     |0     |1     |0     |1     
1     |0     |1     |0     |1     
0     |0     |1     |1     |0     
Clk   |Reset |Set   |Q     |Qn    
0     |1     |0     |1     |0     
1     |1     |0     |1     |0     
0     |1     |0     |0     |1     
Clk   |Reset |Set   |Q     |Qn    
0     |1     |1     |0     |1     
1     |1     |1     |0     |1     
0     |1     |1     |0     |1     

Testing 'FlipFlop' part.
Clk  |Data |Q    |Qn   
0    |0    |0    |1    
1    |0    |0    |1    
0    |0    |0    |1    
Clk  |Data |Q    |Qn   
0    |1    |0    |1    
1    |1    |0    |1    
0    |1    |1    |0    
Clk  |Data |Q    |Qn   
0    |0    |1    |0    
1    |0    |1    |0    
0    |0    |0    |1    
Clk  |Data |Q    |Qn   
0    |1    |0    |1    
1    |1    |0    |1    
0    |1    |1    |0    

Testing 'TFlipFlop' part.
T |Q 
0 |0 
1 |0 
0 |1 
T |Q 
0 |1 
1 |1 
0 |0 

```

# Todo

Alot
