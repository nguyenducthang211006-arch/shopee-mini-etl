USE shopeemini_dwh;
GO

CREATE TABLE etl_watermark (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_watermark DATETIME2(0)
);
GO
--Trigger để lấy thời gian mới thay đổi 
USE shopeemini;
GO

CREATE OR ALTER TRIGGER trg_orderr_updated_at
ON orderr
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    IF UPDATE(updated_at)
        RETURN;

    UPDATE o
    SET o.updated_at = GETDATE()
    FROM orderr o
    INNER JOIN inserted i
        ON o.order_id = i.order_id;
END;
GO
-- Lựa chọn watermark ban đầu là thời gian update_at lớn nhất
USE shopeemini_dwh;
GO

INSERT INTO etl_watermark (
    pipeline_name,
    last_watermark
)
SELECT
    'order_pipeline',
    MAX(updated_at)
FROM shopeemini.dbo.orderr;