extends Spatial

signal fired

enum {
	HIP_FIRE,
	ADS_FIRE,
	RELOADING,
	INACTIVE
}
export var damage = 60
onready var anim_player=$AnimationPlayer
onready var bullet_emitters_base : Spatial = $BulletEmitters
onready var bullet_emitters = $BulletEmitters.get_children()
var fire_point : Spatial
var bodies_to_exclude : Array = []
var hammer_down=false
var ads=false
var reloading = false
var anim_playing=false
var just_fired_bullet=false
var bullet_loaded=false
export var ammo_in_gun =-1
export var ammo_reserve = 11
var lever_forward=false

var state=HIP_FIRE

#TO DO: Make the gun eject unused bullets without having to fire first
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
			if event.button_index==BUTTON_WHEEL_UP and hammer_down==false and anim_playing==false and just_fired_bullet==false and lever_forward==false:
				anim_player.play("HipLeverFowardEmpty")
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if event.button_index==BUTTON_WHEEL_UP and hammer_down==true and anim_playing==false and just_fired_bullet==false and lever_forward==false:
				anim_player.play("HipLeverFowardEmptyHammerDown")
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if event.button_index==BUTTON_WHEEL_UP and hammer_down==false and anim_playing==false and just_fired_bullet==true and lever_forward==false:
				anim_player.play("HipLeverFowardCasing")
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if event.button_index==BUTTON_WHEEL_UP and anim_playing==false and ammo_in_gun<0 and lever_forward==false:
				if hammer_down==false:
					anim_player.play("HipLeverFowardEmpty")
				else:
					anim_player.play("HipLeverFowardEmptyHammerDown")
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if event.button_index==BUTTON_WHEEL_DOWN and hammer_down==true and anim_playing==false and lever_forward==true:
				anim_player.play("HipLeverBack")
				anim_playing=true
				lever_forward=false
				bullet_loaded=true
			if event.button_index==BUTTON_WHEEL_UP and anim_playing==false and ammo_in_gun>=0 and bullet_loaded==true:
				print("success")
				anim_player.play("HipLeverFowardBullet")
				eject_bullet()
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if Input.is_action_just_pressed("attack") and hammer_down==true and anim_playing==false and lever_forward==false:
				fire()
				anim_playing=true
			if Input.is_action_just_pressed("ADS") and state!=ADS_FIRE:
				anim_player.play("HiptoADS")
				anim_playing=true
				ads=true
				state=ADS_FIRE
				return
		if Input.is_action_just_pressed("reload") and state!=RELOADING and anim_playing==false:
			anim_player.play("HiptoReload")
			anim_playing=true
			state=RELOADING
			return
	
	if state==RELOADING:
		if event is InputEventMouseButton:
			if event.button_index==BUTTON_WHEEL_UP:
				insert_bullet()
				return
		if Input.is_action_just_pressed("reload"):
			if ads==false:
				anim_player.play("ReloadtoHip")
				anim_playing=true
				state=HIP_FIRE
				return
			elif ads==true:
				anim_player.play("ReloadtoADS")
				anim_playing=true
				state=ADS_FIRE
				return
	
	if state==ADS_FIRE:
		if event is InputEventMouseButton:
			if event.button_index==BUTTON_WHEEL_UP and hammer_down==false and anim_playing==false and just_fired_bullet==false and lever_forward==false:
				anim_player.play("ADSLeverFowardEmpty")
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if event.button_index==BUTTON_WHEEL_UP and hammer_down==true and anim_playing==false and just_fired_bullet==false and lever_forward==false:
				anim_player.play("ADSLeverFowardEmptyHammerDown")
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if event.button_index==BUTTON_WHEEL_UP and hammer_down==false and anim_playing==false and just_fired_bullet==true and lever_forward==false:
				anim_player.play("ADSLeverFowardCasing")
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if event.button_index==BUTTON_WHEEL_UP and anim_playing==false and ammo_in_gun<0 and lever_forward==false:
				if hammer_down==false:
					anim_player.play("ADSLeverFowardEmpty")
				else:
					anim_player.play("ADSLeverFowardEmptyHammerDown")
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if event.button_index==BUTTON_WHEEL_DOWN and hammer_down==true and anim_playing==false and lever_forward==true:
				anim_player.play("ADSLeverBack")
				anim_playing=true
				lever_forward=false
				bullet_loaded=true
			if event.button_index==BUTTON_WHEEL_UP and anim_playing==false and ammo_in_gun>=0 and bullet_loaded==true:
				print("success")
				anim_player.play("ADSLeverFowardBullet")
				eject_bullet()
				anim_playing=true
				hammer_down=true
				lever_forward=true
				bullet_loaded=false
			if Input.is_action_just_pressed("attack") and hammer_down==true and anim_playing==false and lever_forward==false:
				fire()
				anim_playing=true
			if Input.is_action_just_pressed("ADS") and state==ADS_FIRE:
				anim_player.play("ADStoHip")
				anim_playing=true
				ads=false
				state=HIP_FIRE
				return
		if Input.is_action_just_pressed("reload") and state!=RELOADING and anim_playing==false:
			anim_player.play("ADStoReload")
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
			anim_player.play("HipFire")
			hammer_down=false
			emit_signal("fired")
			ammo_in_gun-=1
			just_fired_bullet=true
			bullet_loaded=false
			#print(ammo_in_gun+1," bullets in gun")
			#print(ammo_reserve+1," bullets spare")
			#TO DO create bullet
			return
		if ads==true:
			anim_player.play("ADSFire")
			hammer_down=false
			emit_signal("fired")
			ammo_in_gun-=1
			just_fired_bullet=true
			bullet_loaded=false
			#TO DO create bullet
			return
	if ammo_in_gun<0:
		if ads==false:
			anim_player.play("HipDryFire")
			hammer_down=false
			just_fired_bullet=false
		if ads==true:
			anim_player.play("ADSDryFire")
			hammer_down=false
			just_fired_bullet=false

func insert_bullet():
	if ammo_in_gun<7 and ammo_reserve>=0:
		anim_player.play("InsertBullet")
		anim_playing=true
		bullet_loaded=true
		return
	return

func reload():
	if ammo_in_gun<7:
		ammo_in_gun+=1
		ammo_reserve-=1
	print(ammo_in_gun+1," bullets in gun")
	#print(ammo_reserve+1," bullets spare")
	return

func eject_bullet():
	if ammo_in_gun>=0:
		ammo_in_gun-=1
		return
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


