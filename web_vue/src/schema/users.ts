import { localStr } from "@/utils";
import { type User, ItemFields, TableColumns } from "@/types";

export const userCols: TableColumns<User>[] = [
  { name: "id", header: "#" },
  { name: "fullname", header: "Пользователь" },
  { name: "username", header: "Логин" },
  { name: "role", header: "Роль" },
  {
    name: "created",
    header: "Создан",
    cell: (row) => localStr(row.created),
  },
];

export const userDivs: ItemFields<User>[] = [
  { key: "fullname", label: "Пользователь" },
  { key: "username", label: "Логин" },
  { key: "role", label: "Роль" },
  {
    key: "created",
    label: "Создан",
    div: (row) => localStr(row.created),
  },
  { key: "attempt", label: "Попыток", div: (row) => String(row.attempt) },
  {
    key: "blocked",
    label: "Блокир.",
    div: (row) => (row.blocked ? "Да" : "Нет"),
  },
  {
    key: "change_pswd",
    label: "Пароль",
    div: (row) => (row.change_pswd ? "Да" : "Нет"),
  },
  {
    key: "deleted",
    label: "Удален",
    div: (row) => (row.deleted ? "Да" : "Нет"),
  },
];
