package main

import (
	"context"
	srv "grpcgo/server"
	//"sync"
	"time"
)

func startServer() {
	srv.GRPCServer()
}

func producer(ctx context.Context, ch chan (int)) {
	ctxSub, can := context.WithTimeout(ctx, time.Second*20)

	defer can()
	for _, i := range []int{1, 2} {
		ch <- i
	}

	select {
	case <-ctxSub.Done():
		println("cancel with timeout")
		return
	}
}

func consumer(ctx context.Context, ch chan (int)) {
	for {
		select {
		case i := <-ch:
			println(i)
		case <-ctx.Done():
			println("cancel")
			return
		}
	}
}

func main() {
	//wg := sync.WaitGroup{}
	ctx, cel := context.WithCancel(context.Background())
	//wg.Add(1)
	ch := make(chan int)
	go consumer(ctx, ch)
	go producer(ctx, ch)
	time.Sleep(5 * time.Second)
	cel()
	time.Sleep(2 * time.Second)
	//wg.Wait()

}
