extends Spatial

signal fired
signal out_of_ammo

enum {
	HIP_FIRE,
	ADS_FIRE,
	RELOADING,
	INACTIVE
}
export var damage= 20
onready var anim_player=$Graphics/AnimationPlayer
onready var cylinder = $Graphics/CylinderPosition
onready var bullet_emitters_base : Spatial = $BulletEmitters
onready var bullet_emitters = $BulletEmitters.get_children()
var fire_point : Spatial
var bodies_to_exclude : Array = []
var hammer_down=false
var ads=false
var reloading = false
var anim_playing=false
var cylinder_starting_pos
var cylinder_pos
export var ammo_in_gun =5
var shells_in_gun=-1
export var ammo_reserve = 11

var state=HIP_FIRE

#TO DO: Make the gun unable to hold more
func _ready():
	state=HIP_FIRE

func init(_fire_point: Spatial, _bodies_to_exclude: Array):
	fire_point=_fire_point
	bodies_to_exclude=_bodies_to_exclude
	for bullet_emitter in bullet_emitters:
		bullet_emitter.set_damage(damage)
		bullet_emitter.set_bodies_to_exclude(bodies_to_exclude)

func _input(event):
	if state==INACTIVE:
		return
	if state==HIP_FIRE:
		if event is InputEventMouseButton:
			if event.button_index==BUTTON_WHEEL_DOWN and hammer_down==false and anim_playing==false:
				anim_player.play("HammerCock")
				#cylinder_starting_pos=cylinder.rotation_degrees.x
				#cylinder.rotation.x-=60
				anim_playing=true
				hammer_down=true
			if event.button_index==BUTTON_WHEEL_UP and hammer_down==true and anim_playing==false:
				anim_player.play("resetGun")
				anim_playing=true
				hammer_down=false
			if Input.is_action_just_pressed("attack") and hammer_down==true and anim_playing==false:
				fire()
				anim_playing=true
			if Input.is_action_just_pressed("ADS") and state!=ADS_FIRE:
				anim_player.play("ADS")
				anim_playing=true
				ads=true
				state=ADS_FIRE
				return
		if Input.is_action_just_pressed("reload") and state!=RELOADING and anim_playing==false:
			anim_player.play("ReloadPosition")
			anim_playing=true
			state=RELOADING
			return
	
	if state==RELOADING:
		if event is InputEventMouseButton:
			if event.button_index==BUTTON_WHEEL_UP:
				insert_bullet()
				return
			if event.button_index==BUTTON_WHEEL_DOWN and ammo_in_gun>=0:
				anim_player.play("RemoveBullet")
				anim_playing=true
			if event.button_index==BUTTON_WHEEL_DOWN and shells_in_gun>=0:
				anim_player.play("RemoveEmptyBullet")
				anim_playing=true
				pass# to do make bullet remove from cylinder
		if Input.is_action_just_pressed("attack") and anim_playing==false:
			anim_player.play("RotateCylinder")
		if Input.is_action_just_pressed("reload"):
			if ads==false:
				anim_player.play("endReloading")
				anim_playing=true
				state=HIP_FIRE
				return
			elif ads==true:
				anim_player.play("endReloadingFromADS")
				anim_playing=true
				state=ADS_FIRE
				return
	
	if state==ADS_FIRE:
		if event is InputEventMouseButton:
			if event.button_index==BUTTON_WHEEL_DOWN and hammer_down==false and anim_playing==false:
				anim_player.play("HammerCockADS")
				anim_playing=true
				hammer_down=true
			if event.button_index==BUTTON_WHEEL_UP and hammer_down==true and anim_playing==false:
				anim_player.play("resetGunADS")
				anim_playing=true
				hammer_down=false
			if Input.is_action_just_pressed("attack") and hammer_down==true and anim_playing==false:
				fire()
				anim_playing=true
			if Input.is_action_just_pressed("ADS") and state==ADS_FIRE:
				anim_player.play("ADSEnd")
				anim_playing=true
				ads=false
				state=HIP_FIRE
				return
		if Input.is_action_just_pressed("reload") and state!=RELOADING and anim_playing==false:
			anim_player.play("ReloadPositionFromADS")
			anim_playing=true
			state=RELOADING
			return



func _on_AnimationPlayer_animation_finished(_anim_name):
	anim_playing=false

func fire():
	if ammo_in_gun>=0:
		var start_transform = bullet_emitters_base.global_transform
		bullet_emitters_base.global_transform = fire_point.global_transform
		for bullet_emitter in bullet_emitters:
			bullet_emitter.fire()
		bullet_emitters_base.global_transform = start_transform
		if ads==false:
			anim_player.play("Shoot")
			hammer_down=false
			emit_signal("fired")
			ammo_in_gun-=1
			print(ammo_in_gun+1," bullets in gun")
			print(shells_in_gun+1," shells in gun")
			print(ammo_reserve+1," bullets spare")
			if shells_in_gun<5:
				shells_in_gun+=1
				return
			#TO DO create bullet
			return
		if ads==true:
			anim_player.play("ShootADS")
			hammer_down=false
			emit_signal("fired")
			ammo_in_gun-=1
			shells_in_gun+=1
			#TO DO create bullet
			return
	if ammo_in_gun<0:
		if ads==false:
			anim_player.play("DryFire")
			hammer_down=false
			emit_signal("out_of_ammo")
			return
		if ads==true:
			anim_player.play("DryFireADS")
			hammer_down=false
			emit_signal("out_of_ammo")
			return

func insert_bullet():
	if ammo_in_gun<5 and ammo_reserve>=0:
		anim_player.play("InsertBullet")
		anim_playing=true
		return

func reload():
	if ammo_in_gun<5:
		ammo_in_gun+=1
	#shells_in_gun+=1
		ammo_reserve-=1
	#print(ammo_in_gun+1," bullets in gun")
	#print(shells_in_gun+1," shells in gun")
	#print(ammo_reserve+1," bullets spare")
	return

func remove_empty_bullet():
	shells_in_gun-=1
	return

func remove_bullet():
	#if shells_in_gun>=0:
	#	shells_in_gun-=1
	if ammo_in_gun>=0:
		ammo_in_gun-=1
	return

func set_active():
	state=HIP_FIRE
	show()

func set_inactive():
	state=INACTIVE
	anim_player.play("Idle")
	hide()

func is_idle():
	return !anim_player.is_playing() or anim_player.current_animation=="Idle"
