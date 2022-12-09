package main

import (
	"encoding/json"
	"fmt"
	"grpcgo/orm/models"
	"log"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func main() {
	db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// 迁移 schema
	db.AutoMigrate(&models.Volume{}, &models.VirtualMachine{}, &models.Tenant{}, &models.Tenant{})
	//db.AutoMigrate()

	//disk := &models.Volume{Name: "OS-Root", Size: 1024, Type: 1, VirtualMachineID: 1}
	//vm := &models.VirtualMachine{Cpu: 2, Memory: 10, Disks: []models.Volume{{Size: 4, Name: "os-disk4", Type: 2}}}
	//res := db.Create(&disk)
	//var volume models.Volume
	//var volume models.Volume
	//disk := models.Volume{}
	//
	//vm := models.VirtualMachine{}
	//res := vm.Create(db)

	//vm := models.VirtualMachine{ID: 1}
	//res := vm.Query(db)
	//if res != nil {
	//	log.Fatal(res)
	//}
	/* 	tenant := models.Tenant{Name: "PG", Datacenter: []models.Datacenter{{Name: "ATC", Location: "Altlanta", Dual: true},
	   		{Name: "EDC", Location: "Bolin", Dual: false}}}
	   	if err := tenant.Create(db); err != nil {
	   		log.Fatal(err)
	   	} */
	/* 	tenant := models.Tenant{Name: "PG"}
	   	if err := tenant.Query(db); err != nil {
	   		log.Fatal(err)
	   	} */

	dcs := []models.Datacenter{}
	db.Find(&dcs)
	tenant := models.Tenant{Name: "QA", Datacenter: dcs}
	if err := tenant.Create(db); err != nil {
		log.Fatal(err)
	}
	e, err := json.Marshal(tenant)

	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(e))
	//db.Create(&models.VirtualMachine{Cpu: 2, Memory: 10})
}
