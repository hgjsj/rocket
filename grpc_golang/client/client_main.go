package main

import (
	"context"
	"fmt"
	"google.golang.org/grpc"
	pb "grpcgo/server/dataObj"
	"io"
	"log"
)

const (
	address = "localhost:8088"
)

func main() {

	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	c := pb.NewVirtualMachineClient(conn)
	v := pb.NewVolumesClient(conn)
	//ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	//defer cancel()

	r, err := c.CreateVM(context.Background(), &pb.VM{Cpu: 2, Memory: 2, Disks: make([]*pb.Volume, 1, 1)})

	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	fmt.Println(r)

	stream, err := v.ListVolumes(context.Background(), &pb.Empty{})

	for {
		vol, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("%v.ListFeatures(_) = _, %v", v, err)
		}

		fmt.Printf("Disk name: %s, Size: %d, Type: %s\n", vol.GetName(), vol.GetSize(), pb.Volume_Type_name[int32(vol.GetType())])
	}

}
