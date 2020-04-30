/*
MIT License

Copyright  (c) 2009-2019 easyice

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/



/*
二分查找
a: 待查找的数组
x:要查找的元素
nSize 数组a的大小
return:找到了返回位置，否则返回 -1
*/

template<class Type>
int BinarySearch(Type a[],const Type& x,int nSize) 

{ 
	if (nSize <= 0)
		return -1;
	int left=0; 
	int right=nSize-1; 

	while(left<=right)
	{ 
		int middle=(left+right)/2; 
		if (x==a[middle]) return middle; 
		if (x>a[middle]) left=middle+1; 
		else right=middle-1; 
	} 

	return -1; 
}




