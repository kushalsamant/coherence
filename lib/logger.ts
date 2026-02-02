/**
 * Centralized logging utility for KVSHVL Platform
 * Provides consistent logging across the application with environment-aware behavior
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LoggerConfig {
  enabled: boolean;
  minLevel: LogLevel;
}

const config: LoggerConfig = {
  enabled: process.env.NODE_ENV === 'development' || process.env.PLATFORM_DEBUG === 'true',
  minLevel: process.env.NODE_ENV === 'production' ? 'warn' : 'debug',
};

const levels: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

class Logger {
  private shouldLog(level: LogLevel): boolean {
    return config.enabled && levels[level] >= levels[config.minLevel];
  }

  debug(message: string, ...args: any[]): void {
    if (this.shouldLog('debug')) {
      console.log(`[DEBUG] ${message}`, ...args);
    }
  }

  info(message: string, ...args: any[]): void {
    if (this.shouldLog('info')) {
      console.info(`[INFO] ${message}`, ...args);
    }
  }

  warn(message: string, ...args: any[]): void {
    if (this.shouldLog('warn')) {
      console.warn(`[WARN] ${message}`, ...args);
    }
  }

  error(message: string, error?: Error | unknown, ...args: any[]): void {
    if (this.shouldLog('error')) {
      console.error(`[ERROR] ${message}`, error, ...args);
      
      // In production, you might want to send to error tracking service
      if (process.env.NODE_ENV === 'production') {
        // TODO: Send to error tracking service (Sentry, etc.)
      }
    }
  }
}

export const logger = new Logger();
export default logger;

