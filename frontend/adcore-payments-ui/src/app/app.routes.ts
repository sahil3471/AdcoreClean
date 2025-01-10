import { Routes } from '@angular/router';
import { PaymentsListComponent } from './payments-list/payments-list.component';
import { AddPaymentComponent } from './add-payment/add-payment.component';

export const routes: Routes = [
  { path: '', component: PaymentsListComponent }, // Homepage with payments
  { path: 'add-payment', component: AddPaymentComponent }, // Add Payment page
];
