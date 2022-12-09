package models

import (
	"gorm.io/gorm"
	"time"
)

type VirtualMachine struct {
	ID        uint `gorm:"primarykey"`
	CreatedAt time.Time
	UpdatedAt time.Time
	Cpu       uint32
	Memory    uint32
	Disks     []Volume `gorm:"foreignKey:vm_id"`
}

type Volume struct {
	gorm.Model
	Size             uint64
	Name             string
	Type             uint8
	VirtualMachineID uint `gorm:"column:vm_id"`
}

type Datacenter struct {
	ID       uint `gorm:"primarykey"`
	Name     string
	Location string
	Dual     bool
	Tenants  []Tenant `gorm:"many2many:tenant_datacenter;"`
}

type Tenant struct {
	ID         uint `gorm:"primarykey"`
	CreatedAt  time.Time
	UpdatedAt  time.Time
	Name       string
	Datacenter []Datacenter `gorm:"many2many:tenant_datacenter;"`
}

/*
func (v *Volume) BeforeCreate(tx *gorm.DB) (err error) {
	var volume Volume
	var res = tx.First(&volume, "Name = ?", v.Name)

	if errors.Is(res.Error, gorm.ErrRecordNotFound) {
		return nil
	}
	return gorm.ErrInvalidValue

}
*/

type CRUD interface {
	Create(*gorm.DB) (err error)
	Delete(*gorm.DB) (err error)
	Query(*gorm.DB) (v interface{}, err error)
	Update(*gorm.DB) (err error)
}

func (vm *VirtualMachine) Create(db *gorm.DB) (err error) {
	res := db.Create(vm)
	return res.Error
}

func (vm *VirtualMachine) Query(db *gorm.DB) (err error) {
	res := db.Find(vm)

	if res.Error != nil {
		return res.Error
	}
	volumes := []Volume{}
	err = db.Model(vm).Association("Disks").Find(&volumes)
	vm.Disks = volumes
	return err
}

func (t *Tenant) Create(db *gorm.DB) (err error) {
	res := db.Create(t)
	return res.Error
}

func (t *Tenant) Query(db *gorm.DB) (err error) {
	res := db.Find(t)

	if res.Error != nil {
		return res.Error
	}
	dcs := []Datacenter{}
	err = db.Model(t).Association("Datacenter").Find(&dcs)
	t.Datacenter = dcs
	return err
}

func (dc *Datacenter) Create(db *gorm.DB) (err error) {
	res := db.Create(dc)
	return res.Error
}

func (dc *Datacenter) Query(db *gorm.DB) (err error) {
	res := db.First(dc)

	if res.Error != nil {
		return res.Error
	}
	t := []Tenant{}
	err = db.Model(dc).Association("Tenants").Find(&t)
	dc.Tenants = t
	return err
}
