class Character extends Phaser.Physics.Arcade.Sprite {
    constructor(scene, x, y, texture, name, power) {
        super(scene, x, y, texture);
        
        // Add character to the scene
        scene.add.existing(this);
        scene.physics.add.existing(this);
        
        // Character properties
        this.name = name;
        this.power = power;
        this.isActive = false;
        this.powerActive = false;
        this.powerCooldown = 0;
        this.maxPowerDuration = 100;
        this.powerDuration = this.maxPowerDuration;
        
        // Physics properties
        this.setCollideWorldBounds(true);
        this.setBounce(0.1);
        this.body.setSize(this.width * 0.7, this.height * 0.9);
        
        // Animation states
        this.anims.create({
            key: 'idle',
            frames: this.anims.generateFrameNumbers(texture, { start: 0, end: 0 }),
            frameRate: 10,
            repeat: -1
        });
        
        this.anims.create({
            key: 'walk',
            frames: this.anims.generateFrameNumbers(texture, { start: 0, end: 1 }),
            frameRate: 10,
            repeat: -1
        });
        
        this.anims.create({
            key: 'power',
            frames: this.anims.generateFrameNumbers(texture, { start: 2, end: 3 }),
            frameRate: 10,
            repeat: 0
        });
    }
    
    activate() {
        this.isActive = true;
        this.setTint(0xffffff);
    }
    
    deactivate() {
        this.isActive = false;
        this.setTint(0x888888);
    }
    
    usePower() {
        if (this.powerCooldown <= 0) {
            this.powerActive = true;
            this.anims.play('power', true);
            
            // Power-specific effects will be implemented in subclasses
            
            return true;
        }
        return false;
    }
    
    stopPower() {
        this.powerActive = false;
        this.powerCooldown = 100; // Cooldown time
        this.powerDuration = this.maxPowerDuration;
    }
    
    update(cursors, gameControls) {
        if (!this.isActive) return;
        
        // Handle movement
        const speed = 160;
        
        // Check for keyboard or touch controls
        const left = cursors.left.isDown || gameControls.left;
        const right = cursors.right.isDown || gameControls.right;
        const action = cursors.space.isDown || gameControls.action;
        
        if (left) {
            this.setVelocityX(-speed);
            this.setFlipX(true);
            this.anims.play('walk', true);
        } else if (right) {
            this.setVelocityX(speed);
            this.setFlipX(false);
            this.anims.play('walk', true);
        } else {
            this.setVelocityX(0);
            if (!this.powerActive) {
                this.anims.play('idle', true);
            }
        }
        
        // Jump
        if ((cursors.up.isDown || gameControls.up) && this.body.touching.down) {
            this.setVelocityY(-330);
        }
        
        // Power activation
        if (action) {
            if (!this.powerActive) {
                this.usePower();
            }
        } else if (this.powerActive) {
            this.stopPower();
        }
        
        // Update power cooldown
        if (this.powerCooldown > 0) {
            this.powerCooldown--;
        }
        
        // Update power duration
        if (this.powerActive) {
            this.powerDuration--;
            if (this.powerDuration <= 0) {
                this.stopPower();
            }
        }
    }
}
