class XinNa extends Character {
    constructor(scene, x, y) {
        super(scene, x, y, 'xinna', 'Xin Na', 'time-slow');
        
        // Time manipulation specific properties
        this.timeSlowFactor = 0.3; // How much to slow down time
        this.timeSlowRadius = 200; // Radius of effect
        
        // Time slow visual effect
        this.timeSlowFX = scene.add.graphics();
        this.timeSlowFX.setVisible(false);
    }
    
    usePower() {
        if (super.usePower()) {
            // Apply time slow effect to the scene
            this.scene.timeScale = this.timeSlowFactor;
            
            // Exclude this character from time slow
            this.scene.time.timeScale = 1;
            
            // Visual effect
            this.timeSlowFX.clear();
            this.timeSlowFX.fillStyle(0x0088ff, 0.2);
            this.timeSlowFX.fillCircle(this.x, this.y, this.timeSlowRadius);
            this.timeSlowFX.lineStyle(2, 0x00ffff, 0.8);
            this.timeSlowFX.strokeCircle(this.x, this.y, this.timeSlowRadius);
            this.timeSlowFX.setVisible(true);
            
            // Add time particles
            if (!this.timeParticles) {
                this.timeParticles = this.scene.add.particles(0, 0, 'power-fx', {
                    lifespan: 2000,
                    speed: { min: 20, max: 100 },
                    scale: { start: 0.2, end: 0 },
                    quantity: 2,
                    blendMode: 'ADD',
                    emitting: false
                });
            }
            
            this.timeParticles.setPosition(this.x, this.y);
            this.timeParticles.emitting = true;
            
            return true;
        }
        return false;
    }
    
    stopPower() {
        super.stopPower();
        
        // Reset time scale
        this.scene.timeScale = 1;
        
        // Hide visual effect
        this.timeSlowFX.setVisible(false);
        
        if (this.timeParticles) {
            this.timeParticles.emitting = false;
        }
    }
    
    update(cursors, gameControls) {
        super.update(cursors, gameControls);
        
        // Update time slow effect position
        if (this.powerActive) {
            this.timeSlowFX.clear();
            this.timeSlowFX.fillStyle(0x0088ff, 0.2);
            this.timeSlowFX.fillCircle(this.x, this.y, this.timeSlowRadius);
            this.timeSlowFX.lineStyle(2, 0x00ffff, 0.8);
            this.timeSlowFX.strokeCircle(this.x, this.y, this.timeSlowRadius);
            
            if (this.timeParticles) {
                this.timeParticles.setPosition(this.x, this.y);
            }
        }
    }
}
