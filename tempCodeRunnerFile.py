ture_date_list = rdb.Read_full_date()
            # if len(self.creature_date_list) != 0:
            #     rem_list = rdb.Read_full()

            #     rq = Reminders_queue(self.convert_list(rem_list))
            #     print(rq.get_first_every_day())
            #     if rq.get_first_every_day()[2] == 0:
            #         # self.text_ed = rdb.Read_text_index(
            #         #     rq.get_first_every_day()[0])
            #         th = Worker(rdb.Read_text_index(
            #             rq.get_first_every_day()[0]))
            #         th.start()
            #     rq.clear_queue()