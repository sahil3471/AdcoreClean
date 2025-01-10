// add-payment.component.ts

import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { CommonModule } from '@angular/common'; // Import CommonModule
import { PaymentsService, Payment } from '../payments.service';
import { Router } from '@angular/router'; // Import Router

@Component({
  selector: 'app-add-payment',
  standalone: true,
  imports: [FormsModule, CommonModule], // Include FormsModule and CommonModule
  template: `
    <div class="form-container">
      <h2 class="form-title">Add New Payment</h2>
      <form (ngSubmit)="onSubmit()" #paymentForm="ngForm" class="payment-form">
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input
            type="text"
            id="firstName"
            [(ngModel)]="newPayment.payee_first_name"
            name="firstName"
            placeholder="Enter first name"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input
            type="text"
            id="lastName"
            [(ngModel)]="newPayment.payee_last_name"
            name="lastName"
            placeholder="Enter last name"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="dueAmount">Due Amount</label>
          <input
            type="number"
            id="dueAmount"
            [(ngModel)]="newPayment.due_amount"
            name="dueAmount"
            placeholder="Enter due amount"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="status">Status</label>
          <select
            id="status"
            [(ngModel)]="newPayment.payee_payment_status"
            name="status"
            required
            class="form-select"
          >
            <option value="pending">Pending</option>
            <option value="overdue">Overdue</option>
          </select>
        </div>

        <div class="button-group">
          <button type="submit" class="btn-submit">Add Payment</button>
          <button type="button" class="btn-cancel" (click)="onCancel()">Cancel</button>
        </div>
      </form>
    </div>
  `,
  styles: [
    `
      .form-container {
        max-width: 500px;
        margin: 40px auto;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }

      .form-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-bottom: 20px;
      }

      .payment-form {
        display: flex;
        flex-direction: column;
      }

      .form-group {
        margin-bottom: 15px;
      }

      label {
        font-size: 14px;
        font-weight: 600;
        color: #555;
        margin-bottom: 5px;
        display: block;
      }

      .form-input,
      .form-select {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 5px;
        transition: border-color 0.3s ease;
      }

      .form-input:focus,
      .form-select:focus {
        border-color: #007bff;
        outline: none;
      }

      .button-group {
        display: flex;
        justify-content: space-between;
        gap: 10px;
      }

      .btn-submit,
      .btn-cancel {
        width: 48%;
        padding: 10px;
        font-size: 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }

      .btn-submit {
        background-color: #007bff;
        color: #fff;
      }

      .btn-submit:hover {
        background-color: #0056b3;
      }

      .btn-cancel {
        background-color: #e0e0e0;
        color: #333;
      }

      .btn-cancel:hover {
        background-color: #d6d6d6;
      }
    `,
  ],
})
export class AddPaymentComponent {
  newPayment: Partial<Payment> = {
    payee_first_name: '',
    payee_last_name: '',
    due_amount: 0,
    payee_payment_status: 'pending',
  };

  constructor(private paymentsService: PaymentsService, private router: Router) {}

  onSubmit() {
    if (
      this.newPayment.payee_first_name &&
      this.newPayment.payee_last_name &&
      this.newPayment.due_amount
    ) {
      this.paymentsService.createPayment(this.newPayment as Payment).subscribe({
        next: () => {
          alert('Payment added successfully!');
          this.router.navigate(['/']); // Navigate to the homepage
        },
        error: (err) => {
          console.error('Failed to add payment:', err);
          alert('Failed to add payment. Please try again.');
        },
      });
    } else {
      alert('Please fill in all required fields.');
    }
  }

  onCancel() {
    this.router.navigate(['/']); // Navigate to the homepage
  }
}
