class BootScene extends Phaser.Scene {
    constructor() {
        super({ key: 'BootScene' });
    }

    preload() {
        // Display loading progress
        const progressBar = this.add.graphics();
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0x222222, 0.8);
        progressBox.fillRect(240, 270, 320, 50);
        
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        const loadingText = this.make.text({
            x: width / 2,
            y: height / 2 - 50,
            text: 'Loading...',
            style: {
                font: '20px monospace',
                fill: '#ffffff'
            }
        });
        loadingText.setOrigin(0.5, 0.5);
        
        // Update progress bar as assets load
        this.load.on('progress', function (value) {
            progressBar.clear();
            progressBar.fillStyle(0xffffff, 1);
            progressBar.fillRect(250, 280, 300 * value, 30);
        });
        
        this.load.on('complete', function () {
            progressBar.destroy();
            progressBox.destroy();
            loadingText.destroy();
        });
        
        // Load assets here
        this.load.path = 'game/assets/images/';
        
        // Character sprites (using placeholders for now)
        this.load.spritesheet('hangyi', 'placeholder-player.png', { 
            frameWidth: 50, 
            frameHeight: 50 
        });
        
        this.load.spritesheet('xinna', 'placeholder-player.png', { 
            frameWidth: 50, 
            frameHeight: 50 
        });
        
        this.load.spritesheet('jikairui', 'placeholder-player.png', { 
            frameWidth: 50, 
            frameHeight: 50 
        });
        
        // Game objects and environment
        this.load.image('background', 'placeholder-bg.png');
        this.load.image('platform', 'placeholder-platform.png');
        this.load.image('movable-box', 'placeholder-power.png');
        this.load.image('power-icon', 'placeholder-power.png');
        this.load.image('power-fx', 'placeholder-power.png');
        this.load.image('fire-fx', 'placeholder-power.png');
        this.load.image('water-fx', 'placeholder-power.png');
        this.load.image('time-fx', 'placeholder-power.png');
        
        // UI elements
        this.load.image('button', 'placeholder-power.png');
        this.load.image('character-select', 'placeholder-power.png');
        
        // Audio assets
        this.load.path = 'game/assets/audio/';
        this.load.audio('background-music', 'placeholder-music.mp3');
        this.load.audio('telekinesis-sound', 'placeholder-power.mp3');
        this.load.audio('time-sound', 'placeholder-power.mp3');
        this.load.audio('fire-sound', 'placeholder-power.mp3');
        this.load.audio('water-sound', 'placeholder-power.mp3');
    }

    create() {
        this.scene.start('MenuScene');
    }
}
