class JiKairui extends Character {
    constructor(scene, x, y) {
        super(scene, x, y, 'jikairui', 'Ji Kairui', 'elemental');
        
        // Elemental control specific properties
        this.currentElement = 'fire'; // 'fire' or 'water'
        this.elementPower = 100;
        this.elementRange = 200;
        
        // Elemental visual effects
        this.fireFX = scene.add.particles(0, 0, 'fire-fx', {
            lifespan: 1000,
            speed: { min: 50, max: 100 },
            scale: { start: 0.4, end: 0 },
            quantity: 5,
            blendMode: 'ADD',
            emitting: false
        });
        
        this.waterFX = scene.add.particles(0, 0, 'water-fx', {
            lifespan: 1000,
            speed: { min: 50, max: 100 },
            scale: { start: 0.4, end: 0 },
            quantity: 5,
            blendMode: 'ADD',
            emitting: false
        });
    }
    
    toggleElement() {
        this.currentElement = this.currentElement === 'fire' ? 'water' : 'fire';
        
        // Update character appearance based on element
        if (this.currentElement === 'fire') {
            this.setTint(0xff6666);
        } else {
            this.setTint(0x6666ff);
        }
    }
    
    usePower() {
        if (super.usePower()) {
            // Find objects in range that can be affected by the current element
            const objects = this.scene.interactiveObjects.getChildren();
            const affectedObjects = [];
            
            for (const obj of objects) {
                if (obj.canBeAffectedBy && obj.canBeAffectedBy.includes(this.currentElement)) {
                    const distance = Phaser.Math.Distance.Between(
                        this.x, this.y, obj.x, obj.y
                    );
                    
                    if (distance < this.elementRange) {
                        affectedObjects.push(obj);
                        obj.applyElement(this.currentElement);
                    }
                }
            }
            
            // Activate visual effect
            const fx = this.currentElement === 'fire' ? this.fireFX : this.waterFX;
            fx.setPosition(this.x, this.y);
            fx.emitting = true;
            
            return true;
        }
        return false;
    }
    
    stopPower() {
        super.stopPower();
        
        // Deactivate visual effects
        this.fireFX.emitting = false;
        this.waterFX.emitting = false;
    }
    
    update(cursors, gameControls) {
        super.update(cursors, gameControls);
        
        // Toggle element on down press
        if (Phaser.Input.Keyboard.JustDown(cursors.down) || gameControls.down) {
            this.toggleElement();
        }
        
        // Update elemental effect position
        if (this.powerActive) {
            const fx = this.currentElement === 'fire' ? this.fireFX : this.waterFX;
            const direction = this.flipX ? -1 : 1;
            fx.setPosition(this.x + (direction * 50), this.y - 20);
        }
    }
}
