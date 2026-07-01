//program to print numbers from 1 to 10
#include<stdio.h>
//#include<dos.h>
int main()
{
int i=0,n;
//clrscr();
printf("Enter the number for which you want to print multiplication table\n");
scanf("%d",&n);

for(i=1;i<=10;i++)
    {
//ff        delay(1000);
        printf("%d * %d = %d\n",n, i, n*i);
    }
getch();
return 0;
}
