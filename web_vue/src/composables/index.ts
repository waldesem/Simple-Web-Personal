import { ToastProps } from "@nuxt/ui";

interface ToastComposable {
  add: (options: ToastProps) => void;
}

export function useToasts(toast: ToastComposable) {
  const context = {
    error: ["Ошибка", "i-mi-circle-error"],
    primary: ["Информация", "i-mi-circle-information"],
    secondary: ["Вопрос", "i-mi-circle-help"],
    success: ["Успех", "i-mi-circle-check"],
    info: ["Информация", "i-mi-circle-information"],
    warning: ["Внимание", "i-mi-circle-warning"],
    neutral: ["Предупреждение", "i-mi-circle"],
  };

  function create(
    status: ToastProps["color"] = "error",
    description: string = "Невозможно выполнить действие!",
  ) {
    toast.add({
      title: context[status][0],
      description: description,
      color: status,
      icon: context[status][1],
    });
  }
  return { create };
}
