package main
import (
	"fmt"
	"time"

)

func sum(s []int, c chan int) {
        for _, v := range s {
			c <- v // 把 sum 发送到通道 c
			fmt.Println("put v into chan")
        }
		fmt.Println("task Done!")

		// time.Sleep(5*time.Second)
}

func main() {
        s := []int{7, 2, 8, -9, 4, 0}

        c := make(chan int)
        go sum(s[:len(s)/2], c)
        // go sum(s[len(s)/2:], c)
		for i:=0;i<10;i++ {
			time.Sleep(2*time.Second)
			fmt.Println(<-c)
			
		}

        // fmt.Println(x, y, x+y)
}