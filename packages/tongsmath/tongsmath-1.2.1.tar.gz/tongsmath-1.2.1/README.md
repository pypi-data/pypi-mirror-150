##### Thank you ztz for providing the name！！！
# tongsmath  
## Function  
### func.py  
#### class Func:  
"To use this class, you need put in a function expressions  
like y=x+2,y=x**2+x+3(It must be in the form of y=x)"  
###### def __ init __(self, evl -> function expressions,st=-100 -> x minimum value, ed=100 -> x maximum value,xlwlim=-100 -> The x-axis minimum, xuplim=100 -> The x-axis maximum,ylwlim=-100 -> The y-axis minimum, yuplim=100 -> The y-axis maximum)  
###### def show(self)  
 Displays the function image  
## Primenumber  
### DPF.py   
#### def DPF(n)->list or bool  
Returns the prime factor (list) of n,if b is prime number return False.  
e.g. DPF(48)->[2,2,2,2,3] means 48 = 2\*2\*2\*2*3  
### DPN.py  
#### def prime_number_list(n)->list or bool  
Returns all prime numbers within n,if there is no content in the prime number list return False.  
#### def is_primenumber(n)->bool  
Returns whether n is prime.  
## Simplify  
### sim2ndrt.py  
#### def sim2ndrt(n)->list or int  
Returns the simplified result of sqrt(n).
e.g. sim2ndrt(12)->[2,3] means sqrt(12) = 2 * sqrt(3)  
