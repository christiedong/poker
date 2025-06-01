# poker
A helper for the poker minigame in Tiny Tower Vegas

# Rules

```
    'Royal Flush': 5000,
    'Straight Flush': 1500,
    'Four of a Kind': 600,
    'Full House': 300,
    'Flush': 200,
    'Straight': 125,
    'Three of a Kind': 75,
    'Two Pair': 40,
    'Jacks or Better': 10,
    'No Special Hand': 0
```

# Usage
```
python3 poker.py [card1 card2 card3 card4 card5]
```

# Example
```
python3 poker.py CQ CA SJ H5 D4
```
i.e., ♣Q ♣A ♠J ♥5 ♦4, where H=♥ D=♦ C=♣ S=♠

# Outputs
```
Initial Hand: ♣Q ♣A ♠J ♥5 ♦4
Initial Hand Type: No Special Hand Score: 0

Holding Strategy Analysis:
Cards Held                     Expected Score  Possibilities  
-----------------------------------------------------------------
None                           5.86            1,533,939      
♠J                             7.74            178,365        
♣Q                             7.34            178,365        
♣A                             7.17            178,365        
♥5                             6.28            178,365        
♦4                             6.09            178,365        
♣Q ♣A                          8.82            16,215         
♣Q ♠J                          7.48            16,215         
♣A ♠J                          6.49            16,215         
♥5 ♦4                          5.66            16,215         
♣A ♥5                          5.52            16,215         
♣A ♦4                          5.52            16,215         
♣Q ♥5                          5.15            16,215         
♣Q ♦4                          5.15            16,215         
♠J ♥5                          5.15            16,215         
♠J ♦4                          5.15            16,215         
♣Q ♣A ♠J                       4.84            1,081          
♣A ♥5 ♦4                       4.64            1,081          
♣Q ♣A ♥5                       3.82            1,081          
♣Q ♣A ♦4                       3.82            1,081          
♣Q ♠J ♥5                       3.82            1,081          
♣Q ♠J ♦4                       3.82            1,081          
♣A ♠J ♥5                       3.82            1,081          
♣A ♠J ♦4                       3.82            1,081          
♣Q ♥5 ♦4                       2.79            1,081          
♠J ♥5 ♦4                       2.79            1,081          
♣Q ♣A ♠J ♥5                    1.91            47             
♣Q ♣A ♠J ♦4                    1.91            47             
♣Q ♣A ♥5 ♦4                    1.28            47             
♣Q ♠J ♥5 ♦4                    1.28            47             
♣A ♠J ♥5 ♦4                    1.28            47             
♣Q ♣A ♠J ♥5 ♦4                 0.00            1              

Optimal Strategy:
Cards to Hold: ♣Q ♣A
Expected Score: 8.82
Score Improvement Over Keeping All: 8.82
```
It means that holding ♣Q and ♣A is the optimal choice, resulting in an average of 8.82 rewards over all 16,215 possible changes. 
