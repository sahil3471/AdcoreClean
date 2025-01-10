// app.component.ts

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // Import CommonModule
import { RouterModule } from '@angular/router'; // Import RouterModule

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [CommonModule, RouterModule], // Include RouterModule for router directives
  template: `<router-outlet></router-outlet>`,
  styles: [],
})
export class AppComponent {}
