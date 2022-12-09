package server

import (
	"context"
	"fmt"
	rpc "google.golang.org/grpc"
	pb "grpcgo/server/dataObj"
	handler "grpcgo/server/handler"
	"log"
	"net"
	"strconv"
)

type Server struct {
	pb.UnimplementedVirtualMachineServer
}

type VolumeServer struct {
	pb.UnimplementedVolumesServer
}

func (svr *Server) CreateVM(ctx context.Context, in *pb.VM) (*pb.ResponseString, error) {
	//fmt.Println(ctx)
	return &pb.ResponseString{Response: handler.VMCreator()}, nil
}

func (svr *Server) DeleteVM(ctx context.Context, in *pb.RequestString) (*pb.ResponseString, error) {
	return &pb.ResponseString{Response: handler.VMDelete()}, nil
}

func (vol *VolumeServer) ListVolumes(in *pb.Empty, stream pb.Volumes_ListVolumesServer) error {
	for _, v := range []int{1, 2, 3} {
		stream.Send(&pb.Volume{Name: strconv.Itoa(v), Size: 1024, Type: pb.Volume_Type(v % 2)})
	}
	return nil
}

func GRPCServer() {
	listener, err := net.Listen("tcp", ":8088")
	if err != nil {
		log.Fatalf("lisen failed: %v", err)
	}

	s := rpc.NewServer()
	pb.RegisterVirtualMachineServer(s, &Server{})
	pb.RegisterVolumesServer(s, &VolumeServer{})
	fmt.Println("service lisened port 8088")
	if err := s.Serve(listener); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}

}
