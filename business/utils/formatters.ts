import moment from "moment/moment";

// export const FORMAT = {
//   DATE: "YYYY-MM-DD",
//   TIME: "HH:mm:ss",
//   TIME_MINUTE: "HH:mm",
//   DATE_TIME: "YYYY-MM-DD HH:mm:ss",
// };

// // Format date
// export function formatDate(value: any, format: string | null = null) {
//   if (!value) {
//     return null;
//   }
//   if (format) {
//     return moment(String(value)).format(format);
//   }
//   return moment(String(value)).format(FORMAT.DATE);
// }

// // Format date and time
// export function formatDateTime(value: any, format: string | null = null) {
//   if (!value) {
//     return null;
//   }
//   if (format) {
//     return moment(moment.utc(value)).format(format);
//   }
//   return moment(moment.utc(value)).format(FORMAT.DATE_TIME);
// }

// Format currency
export function formatCurrency(value: number): string {
  if (value === null || value === undefined) {
    return '0 ₫';
  }
  
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value);
}

// Format number
export function formatNumber(value: number): string {
  if (value === null || value === undefined) {
    return '0';
  }
  
  return new Intl.NumberFormat('vi-VN').format(value);
}

// UTC to local date conversions
// export function utcToLocalDate(value: any, format: string | null = null) {
//   if (!value) {
//     return null;
//   }
//   if (format) {
//     return moment(moment.utc(value)).local().format(format);
//   }
//   return moment(moment.utc(value)).local().format(FORMAT.DATE);
// }

// export function utcToLocalDateTime(value: any, format: string | null = null) {
//   if (!value) {
//     return null;
//   }
//   if (format) {
//     return moment(moment.utc(value)).local().format(format);
//   }
//   return moment(moment.utc(value)).local().format(FORMAT.DATE_TIME);
// }

// export function utcToLocalTime(value: any, format: string | null = null) {
//   if (!value) {
//     return null;
//   }
//   if (format) {
//     return moment(moment.utc(value)).local().format(format);
//   }
//   return moment(moment.utc(value)).local().format(FORMAT.TIME);
// }

// export function localToUtcTime(value: any, format: string | null = null) {
//   if (!value) {
//     return null;
//   }
//   if (format) {
//     return moment(value).utc().format(format);
//   }
//   return moment(value).utc().format(FORMAT.TIME);
// }