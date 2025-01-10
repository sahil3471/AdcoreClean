// payments-list.component.ts

import { Component, OnInit } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PaymentsService, Payment, PaymentsResponse } from '../payments.service';
import { RouterModule, Router } from '@angular/router';

@Component({
  selector: 'app-payments-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  providers: [CurrencyPipe],
  templateUrl: './payments-list.component.html',
  styleUrls: ['./payments-list.component.css'],
})
export class PaymentsListComponent implements OnInit {
  payments: Payment[] = [];
  editingId: string | null = null;
  errorMessage: string = '';

  // Pagination
  currentPage: number = 1;
  totalPages: number = 1;
  limit: number = 10;

  // Search and Filter
  searchTerm: string = '';
  filterStatus: string = '';

  // Sorting
  sortField: string = '';
  sortOrder: string = 'asc';

  constructor(private paymentsService: PaymentsService, private router: Router) {}

  ngOnInit() {
    this.fetchPayments();
  }

  fetchPayments() {
    this.paymentsService
      .getPayments(
        this.currentPage,
        this.limit,
        this.searchTerm,
        this.filterStatus,
        this.sortField,
        this.sortOrder
      )
      .subscribe({
        next: (data: PaymentsResponse) => {
          this.payments = data.payments;
          this.totalPages = data.totalPages;
          this.currentPage = data.currentPage;
          console.log('Fetched payments:', data.payments);
          console.log('Total Pages:', data.totalPages);
        },
        error: (err) => {
          console.error('Failed to fetch payments:', err);
          this.errorMessage = 'Failed to load payments. Please try again later.';
        },
      });
  }

  onAddPayment() {
    this.router.navigate(['/add-payment']);
  }

  onEdit(paymentId: string | undefined) {
    this.editingId = paymentId || null;
  }

  onSave(payment: Payment) {
    if (payment.id) {
      this.paymentsService.updatePayment(payment.id, payment).subscribe({
        next: () => {
          alert('Payment updated successfully!');
          this.editingId = null;
          this.fetchPayments();
        },
        error: (err) => {
          console.error('Failed to update payment:', err);
          alert('Failed to update payment. Please try again.');
        },
      });
    }
  }

  onCancelEdit() {
    this.editingId = null;
    this.fetchPayments(); // Refresh to discard changes
  }

  onDelete(paymentId: string | undefined) {
    if (paymentId) {
      if (confirm('Are you sure you want to delete this payment?')) {
        this.paymentsService.deletePayment(paymentId).subscribe({
          next: () => {
            alert('Payment deleted successfully!');
            this.fetchPayments();
          },
          error: (err) => {
            console.error('Failed to delete payment:', err);
            alert('Failed to delete payment. Please try again.');
          },
        });
      }
    }
  }

  // Pagination Controls
  goToPage(page: number) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.fetchPayments();
    }
  }

  previousPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.fetchPayments();
    }
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.fetchPayments();
    }
  }

  // Sorting Controls
  sortBy(field: string) {
    if (this.sortField === field) {
      // Toggle sort order
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortField = field;
      this.sortOrder = 'asc';
    }
    this.fetchPayments();
  }
}
