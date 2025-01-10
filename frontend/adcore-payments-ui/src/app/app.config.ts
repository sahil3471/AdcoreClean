import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { CommonModule } from '@angular/common'; // Ensure CommonModule is included
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),                // Provide routes
    provideHttpClient(withFetch()),       // Enable HTTP client with fetch
    importProvidersFrom(CommonModule),    // Enables *ngFor and *ngIf globally
  ],
};
