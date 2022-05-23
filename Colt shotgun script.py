extends Spatial

signal fired

enum {
	HIP_FIRE,
	ADS_FIRE,
	RELOADING,
	INACTIVE
}
export var damage = 6
onready var anim_player=$AnimationPlayer
onready var bullet_emitters_base : Spatial = $BulletEmitters
onready var bullet_emitters = $BulletEmitters.get_children()
var fire_point : Spatial
var bodies_to_exclude : Array = []
var left_hammer_down=false
var right_hammer_down=false
var ads=false
var reloading = false
var anim_playing=false
var left_loaded=false
var right_loaded=false
var just_fired_left=false
var just_fired_right=false
export var ammo_in_gun =-1
export var ammo_reserve = 11

var state=HIP_FIRE

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
			if event.button_index==BUTTON_WHEEL_DOWN and anim_playing==false and left_hammer_down==false and right_hammer_down==false:
				anim_player.play("HipCockHammerL")
				anim_playing=true
				left_hammer_down=true
				return
			elif event.button_index==BUTTON_WHEEL_DOWN and anim_playing==false and left_hammer_down==true and right_hammer_down==false:
				anim_player.play("HipCockHammerR")
				anim_playing=true
				right_hammer_down=true
				return
			elif event.button_index==BUTTON_WHEEL_DOWN and anim_playing==false and left_hammer_down==false and right_hammer_down==true:
				anim_player.play("HipCockHammerL")
				anim_playing=true
				left_hammer_down=true
				return
			elif event.button_index==BUTTON_WHEEL_DOWN and anim_playing==false and left_hammer_down==true and right_hammer_down==true:
				return
			elif event.button_index==BUTTON_WHEEL_UP and anim_playing==false and left_hammer_down==true and right_hammer_down==true:
				anim_player.play("HipDecockHammers")
				anim_playing=true
				left_hammer_down=false
				right_hammer_down=false
				return
			elif event.button_index==BUTTON_WHEEL_UP and anim_playing==false and left_hammer_down==true and right_hammer_down==false:
				anim_player.play("HipDecockHammerL")
				anim_playing=true
				left_hammer_down=false
			elif event.button_index==BUTTON_WHEEL_UP and anim_playing==false and left_hammer_down==false and right_hammer_down==true:
				anim_player.play("HipDecockHammerR")
				anim_playing=true
				right_hammer_down=false
				return
			if Input.is_action_just_pressed("ADS") and state!=ADS_FIRE:
				anim_player.play("HiptoADS")
				anim_playing=true
				ads=true
				state=ADS_FIRE
				return
		if Input.is_action_just_pressed("reload") and state!=RELOADING and anim_playing==false:
			if left_loaded==false and right_loaded==false and just_fired_left==false and just_fired_right==false:# EMPTY RELOAD
				anim_player.play("HipToReload")
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==true and just_fired_left==false and just_fired_right==false:# FULL RELOAD- NONE SHOT
				anim_player.play("HipToReload_Eject_NoneBothLoaded")
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==true and just_fired_left==true and just_fired_right==true:# EJECT BOTH
				anim_player.play("HipToReload_Eject_Both")
				anim_playing=true
				left_loaded=false
				right_loaded=false
				just_fired_left=false
				just_fired_right=false
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==true and just_fired_left==true and just_fired_right==false:# EJECT LEFT, LOADED R
				anim_player.play("HipToReload_Eject_LKeepR")
				left_loaded=false
				just_fired_left=false
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==true and just_fired_left==false and just_fired_right==true:# EJECT RIGHT keep left
				anim_player.play("HipToReload_Eject_RKeepL")
				right_loaded=false
				just_fired_right=false
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==false and right_loaded==true and just_fired_left==false and just_fired_right==true:# EJECT RIGHT empty Left
				anim_player.play("HipToReload_Eject_REmptyL")
				right_loaded=false
				just_fired_right=false
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==false and just_fired_left==true:# EJECT L, EMPTY R
				anim_player.play(("HipToReload_Eject_LEmptyR"))
				left_loaded=false
				just_fired_left=false
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==false and right_loaded==true:# Empty left, loaded Right
				anim_player.play("HipToReload_Eject_NoneRightLoaded")
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==false and just_fired_left==false:# Empty left, loaded Right
				anim_player.play("HipToReload_Eject_NoneLeftLoaded")
				anim_playing=true
				state=RELOADING
				return
		if Input.is_action_just_pressed("attack"):
			if left_loaded==true and left_hammer_down==true and just_fired_left==false:# FIRE LEFT (loaded right Right)
				anim_player.play("HipFireL")
				fire()
				anim_playing=true
				left_hammer_down=false
				just_fired_left=true
				emit_signal("fired")
				return
			elif right_loaded==true and right_hammer_down==true and just_fired_right==false:# FIRE RIGHT (loaded right left)
				anim_player.play("HipFireR")
				fire()
				anim_playing=true
				right_hammer_down=false
				just_fired_right=true
				emit_signal("fired")
				return
			elif left_loaded==true and left_hammer_down==false and just_fired_left==true and right_loaded==true and right_hammer_down==true and just_fired_right==false:# FIRE RIGHT (just shot left)
				anim_player.play("HipFireR")
				fire()
				anim_playing=true
				right_hammer_down=false
				just_fired_right=true
				emit_signal("fired")
				return
			elif left_loaded==false and left_hammer_down==false and right_loaded==true and right_hammer_down==true and just_fired_right==false:# FIRE RIGHT (empty left)
				anim_player.play("HipFireR")
				fire()
				anim_playing=true
				right_hammer_down=false
				just_fired_right=true
				emit_signal("fired")
				return
			elif left_loaded==true and left_hammer_down==false and right_loaded==true and right_hammer_down==true and just_fired_right==false:# FIRE RIGHT (LEFT not cocked)
				anim_player.play("HipFireR")
				fire()
				anim_playing=true
				right_hammer_down=false
				just_fired_right=true
				emit_signal("fired")
				return
			elif left_loaded==false and left_hammer_down==true:
				anim_player.play("HipDryFireL")
				anim_playing=true
				left_hammer_down=false
				return
			elif left_loaded==true and left_hammer_down==true and just_fired_left==true:
				anim_player.play("HipDryFireL")
				anim_playing=true
				left_hammer_down=false
				return
			elif right_loaded==false and right_hammer_down==true:
				anim_player.play("HipDryFireR")
				anim_playing=true
				right_hammer_down=false
				return
			elif right_loaded==true and right_hammer_down==true and just_fired_right==true:
				anim_player.play("HipDryFireR")
				anim_playing=true
				right_hammer_down=false
				return
	if state==RELOADING:
		if event is InputEventMouseButton:
			if event.button_index==BUTTON_WHEEL_UP:
				if left_loaded==false and right_loaded==false and anim_playing==false and ammo_reserve>0:
					anim_player.play("InsertShell_L_RUnloaded")
					anim_playing=true
					left_loaded=true
					insert_shell()
					return
				elif left_loaded==false and right_loaded==true and anim_playing==false and ammo_reserve>0:
					anim_player.play("InsertShell_L_RLoaded")
					anim_playing=true
					left_loaded=true
					insert_shell()
					return
				elif right_loaded==false and anim_playing==false and ammo_reserve>0:
					anim_player.play("InsertShell_R")
					anim_playing=true
					right_loaded=true
					insert_shell()
					return
				elif left_loaded==true and right_loaded==true:
					pass
					return
			#if event.button_index==BUTTON_WHEEL_DOWN:
		if Input.is_action_just_pressed("reload"):
			if ads==false:
				anim_player.play("ReloadToHip")
				anim_playing=true
				print("ammo is", ammo_reserve)
				state=HIP_FIRE
				return
			elif ads==true:
				anim_player.play("ReloadToADS")
				anim_playing=true
				state=ADS_FIRE
				return
	
	if state==ADS_FIRE:
		if event is InputEventMouseButton:
			if event.button_index==BUTTON_WHEEL_DOWN and anim_playing==false and left_hammer_down==false and right_hammer_down==false:
				anim_player.play("ADSCockHammerL")
				anim_playing=true
				left_hammer_down=true
				return
			elif event.button_index==BUTTON_WHEEL_DOWN and anim_playing==false and left_hammer_down==true and right_hammer_down==false:
				anim_player.play("ADSCockHammerR")
				anim_playing=true
				right_hammer_down=true
				return
			elif event.button_index==BUTTON_WHEEL_DOWN and anim_playing==false and left_hammer_down==false and right_hammer_down==true:
				anim_player.play("ADSCockHammerL")
				anim_playing=true
				left_hammer_down=true
				return
			elif event.button_index==BUTTON_WHEEL_DOWN and anim_playing==false and left_hammer_down==true and right_hammer_down==true:
				return
			elif event.button_index==BUTTON_WHEEL_UP and anim_playing==false and left_hammer_down==true and right_hammer_down==true:
				anim_player.play("ADSDeCockHammers")
				anim_playing=true
				left_hammer_down=false
				right_hammer_down=false
				return
			elif event.button_index==BUTTON_WHEEL_UP and anim_playing==false and left_hammer_down==true and right_hammer_down==false:
				anim_player.play("ADSDecockHammerL")
				anim_playing=true
				left_hammer_down=false
			elif event.button_index==BUTTON_WHEEL_UP and anim_playing==false and left_hammer_down==false and right_hammer_down==true:
				anim_player.play("ADSDecockHammerR")
				anim_playing=true
				right_hammer_down=false
				return
			if Input.is_action_just_pressed("ADS") and state==ADS_FIRE:
				anim_player.play("ADStoHip")
				anim_playing=true
				ads=false
				state=HIP_FIRE
				return
		if Input.is_action_just_pressed("reload") and state!=RELOADING and anim_playing==false:
			if left_loaded==false and right_loaded==false and just_fired_left==false and just_fired_right==false:# EMPTY RELOAD
				anim_player.play("ADSToReload")
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==true and just_fired_left==false and just_fired_right==false:# FULL RELOAD- NONE SHOT
				anim_player.play("ADSToReload_Eject_NoneBothLoaded")
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==true and just_fired_left==true and just_fired_right==true:# EJECT BOTH
				anim_player.play("ADSToReload_Eject_Both")
				anim_playing=true
				left_loaded=false
				right_loaded=false
				just_fired_left=false
				just_fired_right=false
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==true and just_fired_left==true and just_fired_right==false:# EJECT LEFT, LOADED R
				anim_player.play("ADSToReload_Eject_LKeepR")
				left_loaded=false
				just_fired_left=false
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==true and just_fired_left==false and just_fired_right==true:# EJECT RIGHT keep left
				anim_player.play("ADSToReload_Eject_RKeepL")
				right_loaded=false
				just_fired_right=false
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==false and right_loaded==true and just_fired_left==false and just_fired_right==true:# EJECT RIGHT empty Left
				anim_player.play("ADSToReload_Eject_REmptyL")
				right_loaded=false
				just_fired_right=false
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==false and just_fired_left==true:# EJECT L, EMPTY R
				anim_player.play(("ADSToReload_Eject_LEmptyR"))
				left_loaded=false
				just_fired_left=false
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==false and right_loaded==true:# Empty left, loaded Right
				anim_player.play("ADSToReload_Eject_NoneRightLoaded")
				anim_playing=true
				state=RELOADING
				return
			elif left_loaded==true and right_loaded==false and just_fired_left==false:# Empty left, loaded Right
				anim_player.play("ADSToReload_Eject_NoneLeftLoaded")
				anim_playing=true
				state=RELOADING
				return
		if Input.is_action_just_pressed("attack"):
			if left_loaded==true and left_hammer_down==true and just_fired_left==false:# FIRE LEFT (loaded right Right)
				anim_player.play("ADSFireL")
				fire()
				anim_playing=true
				left_hammer_down=false
				just_fired_left=true
				emit_signal("fired")
				return
			elif right_loaded==true and right_hammer_down==true and just_fired_right==false:# FIRE RIGHT (loaded right left)
				anim_player.play("ADSFireR")
				fire()
				anim_playing=true
				right_hammer_down=false
				just_fired_right=true
				emit_signal("fired")
				return
			elif left_loaded==true and left_hammer_down==false and just_fired_left==true and right_loaded==true and right_hammer_down==true and just_fired_right==false:# FIRE RIGHT (just shot left)
				anim_player.play("ADSFireR")
				fire()
				anim_playing=true
				right_hammer_down=false
				just_fired_right=true
				emit_signal("fired")
				return
			elif left_loaded==false and left_hammer_down==false and right_loaded==true and right_hammer_down==true and just_fired_right==false:# FIRE RIGHT (empty left)
				anim_player.play("ADSFireR")
				fire()
				anim_playing=true
				right_hammer_down=false
				just_fired_right=true
				emit_signal("fired")
				return
			elif left_loaded==true and left_hammer_down==false and right_loaded==true and right_hammer_down==true and just_fired_right==false:# FIRE RIGHT (LEFT not cocked)
				anim_player.play("ADSFireR")
				fire()
				anim_playing=true
				right_hammer_down=false
				just_fired_right=true
				emit_signal("fired")
				return
			elif left_loaded==false and left_hammer_down==true:
				anim_player.play("ADSDryFireL")
				anim_playing=true
				left_hammer_down=false
				return
			elif left_loaded==true and left_hammer_down==true and just_fired_left==true:
				anim_player.play("ADSDryFireL")
				anim_playing=true
				left_hammer_down=false
				return
			elif right_loaded==false and right_hammer_down==true:
				anim_player.play("ADSDryFireR")
				anim_playing=true
				right_hammer_down=false
				return
			elif right_loaded==true and right_hammer_down==true and just_fired_right==true:
				anim_player.play("ADSDryFireR")
				anim_playing=true
				right_hammer_down=false
				return

func fire():
		var start_transform = bullet_emitters_base.global_transform
		bullet_emitters_base.global_transform = fire_point.global_transform
		for bullet_emitter in bullet_emitters:
			bullet_emitter.fire()
		bullet_emitters_base.global_transform = start_transform

func _on_AnimationPlayer_animation_finished(_anim_name):
	anim_playing=false



func reload():
	if ammo_in_gun<1:
		ammo_in_gun+=1
		ammo_reserve-=1
	print(ammo_in_gun+1," shells in gun")
	#print(ammo_reserve+1," bullets spare")
	return

func insert_shell():
	ammo_reserve-=1
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


