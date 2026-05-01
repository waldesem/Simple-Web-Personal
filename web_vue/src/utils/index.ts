import { useStorage } from "@vueuse/core";

export const flag = useStorage("flag", false, sessionStorage);

export function capitalize(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function localStr(data: string): string {
  return data ? new Date(data).toLocaleDateString() : "";
}

export function timeAgoStr(dateInput: string) {
  const date = typeof dateInput === "string" ? new Date(dateInput) : dateInput;
  const now = Date.now();
  const diffInMs = now - date.getTime();
  const diffInSeconds = Math.floor(diffInMs / 1000);

  // Меньше минуты
  if (diffInSeconds < 60) {
    return "менее минуты назад";
  }

  // Меньше часа (но больше минуты)
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) {
    return diffInMinutes + " минут назад";
  }

  // Менее суток (но больше часа)
  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) {
    return diffInHours + " часов назад";
  }

  const diffInDays = Math.floor(diffInHours / 24);
  if (diffInDays < 30) {
    return diffInDays + " дней назад";
  }
  if (diffInDays < 365) {
    return Math.floor(diffInDays / 30) + " месяцев назад";
  }
  return Math.floor(diffInDays / 365) + " года назад";
}

export const conclusions = {
  agreed: "СОГЛАСОВАНО",
  comments: "СОГЛАСОВАНО С КОММЕНТАРИЕМ",
  cancel: "СНЯТ С ПРОВЕРКИ",
  denied: "ОТКАЗАНО В СОГЛАСОВАНИИ",
};

export const decisions = {
  agreed: "БЕЗ ЗАМЕЧАНИЙ",
  comments: "С КОММЕНТАРИЯМИ",
  cancel: "ОТКАЗ ОТ ПРОВЕРКИ",
  denied: "НЕГАТИВ",
};
