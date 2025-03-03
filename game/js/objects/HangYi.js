class HangYi extends Character {
    constructor(scene, x, y) {
        super(scene, x, y, 'hangyi', 'Hang Yi', 'telekinesis');
        
        // Telekinesis specific properties
        this.telekinesisPower = 100;
        this.telekinesisRange = 150;
        this.heldObject = null;
        
        // Telekinesis visual effect
        this.telekinesisFX = scene.add.particles(0, 0, 'power-fx', {
            lifespan: 1000,
            speed: { min: 10, max: 50 },
            scale: { start: 0.5, end: 0 },
            quantity: 1,
            blendMode: 'ADD',
            emitting: false
        });
    }
    
    usePower() {
        if (super.usePower()) {
            // Find objects in range that can be moved
            const objects = this.scene.interactiveObjects.getChildren();
            let closestObject = null;
            let closestDistance = this.telekinesisRange;
            
            for (const obj of objects) {
                if (obj.canBeMoved) {
                    const distance = Phaser.Math.Distance.Between(
                        this.x, this.y, obj.x, obj.y
                    );
                    
                    if (distance < closestDistance) {
                        closestDistance = distance;
                        closestObject = obj;
                    }
                }
            }
            
            if (closestObject) {
                this.heldObject = closestObject;
                this.heldObject.setTint(0x00ffff);
                
                // Activate visual effect
                this.telekinesisFX.setPosition(this.heldObject.x, this.heldObject.y);
                this.telekinesisFX.emitting = true;
            }
            
            return true;
        }
        return false;
    }
    
    stopPower() {
        super.stopPower();
        
        if (this.heldObject) {
            this.heldObject.clearTint();
            this.heldObject = null;
        }
        
        // Deactivate visual effect
        this.telekinesisFX.emitting = false;
    }
    
    update(cursors, gameControls) {
        super.update(cursors, gameControls);
        
        // Update held object position
        if (this.powerActive && this.heldObject) {
            // Calculate target position (in front of the character)
            const direction = this.flipX ? -1 : 1;
            const targetX = this.x + (direction * 100);
            const targetY = this.y - 50;
            
            // Move object towards target position
            const dx = targetX - this.heldObject.x;
            const dy = targetY - this.heldObject.y;
            
            this.heldObject.x += dx * 0.1;
            this.heldObject.y += dy * 0.1;
            
            // Update particle effect position
            this.telekinesisFX.setPosition(this.heldObject.x, this.heldObject.y);
        }
    }
}
