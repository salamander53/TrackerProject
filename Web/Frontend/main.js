import { app, BrowserWindow } from 'electron';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { spawn } from 'child_process';

// Chuyển đổi import.meta.url thành __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let djangoServer;

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadURL('http://localhost:5173'); // Vite chạy trên cổng 3000

  // Mã hóa đường dẫn chứa các ký tự đặc biệt
  const encodedPath = encodeURIComponent(__dirname);
  djangoServer = spawn('python', ['manage.py', 'runserver'], { cwd: decodeURIComponent(encodedPath) });

  djangoServer.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  djangoServer.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  djangoServer.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', () => {
  djangoServer.kill();
});
