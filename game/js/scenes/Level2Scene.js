class Level2Scene extends Phaser.Scene {
    constructor() {
        super({ key: 'Level2Scene' });
        
        // Level properties
        this.timeScale = 1;
        this.activeCharacterIndex = 0;
    }

    create() {
        // Set up the level
        this.add.text(400, 50, 'Level 2: The Challenge', { 
            fontFamily: 'Arial', 
            fontSize: '32px', 
            color: '#ffffff',
            stroke: '#000000',
            strokeThickness: 4
        }).setOrigin(0.5).setScrollFactor(0).setDepth(100);
        
        // Create the world
        this.createWorld();
        
        // Create characters
        this.createCharacters();
        
        // Set up camera
        this.cameras.main.setBounds(0, 0, 1600, 600);
        this.cameras.main.startFollow(this.characters[this.activeCharacterIndex], true, 0.1, 0.1);
        
        // Set up controls
        this.cursors = this.input.keyboard.createCursorKeys();
        
        // Global game controls state that scenes can access
        this.gameControls = window.gameControls || {
            left: false,
            right: false,
            up: false,
            down: false,
            action: false
        };
        
        // Character switching controls
        this.input.keyboard.on('keydown-ONE', () => this.switchCharacter(0));
        this.input.keyboard.on('keydown-TWO', () => this.switchCharacter(1));
        this.input.keyboard.on('keydown-THREE', () => this.switchCharacter(2));
        
        // Character switching UI
        this.createCharacterSwitchUI();
        
        // Level objective text
        this.objectiveText = this.add.text(400, 100, 'Objective: Complete Ji Kairui\'s elemental trials', { 
            fontFamily: 'Arial', 
            fontSize: '18px', 
            color: '#ffffff',
            backgroundColor: '#000000',
            padding: { x: 10, y: 5 }
        }).setOrigin(0.5).setScrollFactor(0).setDepth(100);
        
        // Add a button to go back to menu (for testing)
        const menuButton = this.add.text(700, 50, 'Back to Menu', { 
            fontFamily: 'Arial', 
            fontSize: '16px', 
            color: '#ffffff',
            backgroundColor: '#880000',
            padding: { x: 10, y: 5 }
        }).setOrigin(0.5).setScrollFactor(0).setDepth(100);
        
        menuButton.setInteractive({ useHandCursor: true });
        menuButton.on('pointerdown', () => {
            this.scene.start('MenuScene');
        });
    }
    
    createWorld() {
        // Add background
        this.add.image(0, 0, 'background').setOrigin(0, 0).setScale(2).setTint(0x886644);
        
        // Create platforms group
        this.platforms = this.physics.add.staticGroup();
        
        // Create ground
        this.platforms.create(400, 580, 'platform').setScale(4, 1).refreshBody().setTint(0x886644);
        
        // Create some platforms
        this.platforms.create(600, 450, 'platform').setTint(0x886644);
        this.platforms.create(50, 350, 'platform').setTint(0x886644);
        this.platforms.create(750, 300, 'platform').setTint(0x886644);
        this.platforms.create(400, 200, 'platform').setTint(0x886644);
        
        // Create interactive objects group
        this.interactiveObjects = this.physics.add.group({
            allowGravity: true,
            bounceY: 0.2
        });
        
        // Add some movable boxes
        for (let i = 0; i < 3; i++) {
            const box = this.interactiveObjects.create(200 + (i * 100), 100, 'movable-box');
            box.canBeMoved = true;
            box.setCollideWorldBounds(true);
            box.setBounce(0.2);
            box.setFriction(1);
        }
        
        // Add some elemental objects
        // Fire chamber objects
        const fireObject1 = this.interactiveObjects.create(500, 100, 'movable-box').setTint(0xff0000);
        fireObject1.canBeAffectedBy = ['water'];
        fireObject1.applyElement = function(element) {
            if (element === 'water') {
                this.setTint(0x888888);
                this.extinguished = true;
            }
        };
        
        // Water chamber objects
        const waterObject1 = this.interactiveObjects.create(700, 100, 'movable-box').setTint(0x0000ff);
        waterObject1.canBeAffectedBy = ['fire'];
        waterObject1.applyElement = function(element) {
            if (element === 'fire') {
                this.setTint(0x888888);
                this.evaporated = true;
            }
        };
        
        // Ice objects
        const iceObject1 = this.interactiveObjects.create(900, 100, 'movable-box').setTint(0x00ffff);
        iceObject1.canBeAffectedBy = ['fire'];
        iceObject1.applyElement = function(element) {
            if (element === 'fire') {
                this.setTint(0x888888);
                this.melted = true;
            }
        };
        
        // Set up collisions
        this.physics.add.collider(this.interactiveObjects, this.platforms);
        this.physics.add.collider(this.interactiveObjects, this.interactiveObjects);
    }
    
    createCharacters() {
        // Create character instances
        this.hangYi = new HangYi(this, 100, 450);
        this.xinNa = new XinNa(this, 200, 450);
        this.jiKairui = new JiKairui(this, 300, 450);
        
        // Store characters in an array for easy access
        this.characters = [this.hangYi, this.xinNa, this.jiKairui];
        
        // Set up collisions for all characters
        for (const character of this.characters) {
            this.physics.add.collider(character, this.platforms);
            this.physics.add.collider(character, this.interactiveObjects);
        }
        
        // Activate the first character
        this.switchCharacter(0);
    }
    
    createCharacterSwitchUI() {
        // Create character switch buttons
        const buttonY = 550;
        const buttonSpacing = 100;
        
        this.characterButtons = [];
        
        for (let i = 0; i < this.characters.length; i++) {
            const character = this.characters[i];
            const x = 50 + (i * buttonSpacing);
            
            const button = this.add.text(x, buttonY, character.name, {
                fontFamily: 'Arial',
                fontSize: '16px',
                color: '#ffffff',
                backgroundColor: i === this.activeCharacterIndex ? '#880000' : '#000000',
                padding: { x: 10, y: 5 }
            }).setScrollFactor(0).setDepth(100);
            
            button.setInteractive({ useHandCursor: true });
            button.on('pointerdown', () => {
                this.switchCharacter(i);
            });
            
            this.characterButtons.push(button);
        }
    }
    
    switchCharacter(index) {
        if (index >= 0 && index < this.characters.length) {
            // Deactivate current character
            this.characters[this.activeCharacterIndex].deactivate();
            this.characterButtons[this.activeCharacterIndex].setBackgroundColor('#000000');
            
            // Activate new character
            this.activeCharacterIndex = index;
            this.characters[this.activeCharacterIndex].activate();
            this.characterButtons[this.activeCharacterIndex].setBackgroundColor('#880000');
            
            // Update camera to follow new active character
            this.cameras.main.startFollow(this.characters[this.activeCharacterIndex], true, 0.1, 0.1);
        }
    }

    update() {
        // Apply time scale
        this.physics.world.timeScale = this.timeScale;
        
        // Update all characters
        for (const character of this.characters) {
            character.update(this.cursors, this.gameControls);
        }
        
        // Reset game controls for next frame
        this.gameControls = {
            left: false,
            right: false,
            up: false,
            down: false,
            action: false
        };
        
        // Check if we should update the global game controls
        if (window.gameControls) {
            this.gameControls = window.gameControls;
        }
    }
}
